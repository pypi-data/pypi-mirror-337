import argparse
import os
import time
import sys
import subprocess
from .shader import Shader
from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()

def cli():
	parser = argparse.ArgumentParser(prog = "pyksh", description="pyksh - ksh compiler in Python")
	parser.add_argument("file1", type=str, help="input file 1")
	parser.add_argument("file2", type=str, help="input file 2", default=None, nargs="?")
	parser.add_argument("-o", "--output", type=str, help="output file", required=False)
	parser.add_argument("-w", "--watch", action="store_true", help="watch input file changes", required=False)
	parser.add_argument("-d", "--decompile", action="store_true", help="decompile ksh to vs and ps")
	parser.add_argument("--validator", help="path to glslangValidator")

	args = parser.parse_args()
	file1 = args.file1
	file2 = args.file2
	output = args.output
	decompile = args.decompile
	watch = args.watch

	if decompile:
		if not os.path.exists(file1):
			print(f"File not exists: {file1}")
			return 1
		fullpath = os.path.abspath(file1)
		dirname = os.path.dirname(fullpath)
		shader = Shader.from_file(file1)
		vs = os.path.join(dirname, shader.vs_name)
		ps = os.path.join(dirname, shader.ps_name)
		with open(vs, "w") as f:
			f.write(shader.vs_content)
			print("write: ", vs)
		with open(ps, "w") as f:
			f.write(shader.ps_content)
			print("write: ", ps)
	
		return 0

	def init_validator():
		# we check validator binary here
		v = args.validator
		if v is None:
			return lambda *_: ""

		p = subprocess.run([v, "--version"], capture_output = True, text = True, check = False)
		if p.returncode != 0:
			print(Fore.RED + "ERROR: validator not valid", Style.RESET_ALL)
			print(p.stdout + p.stderr, flush = True)
			sys.exit(1)
		elif "Glslang Version:" not in p.stdout:
			print(Fore.YELLOW + "WARNING: version string not found, did you provide glslangValidator?", Style.RESET_ALL)
		
		def fn(s, stage):
			p = subprocess.run([v, s, "-S", stage], capture_output = True, text = True)
			return p.stdout + p.stderr
		return fn

	try:
		validate = init_validator()
	except Exception as e:
		raise
	
	mt = [0, 0]
	def watch_loop():
		nonlocal mt
		while True:
			try:
				time.sleep(0.5)
			except KeyboardInterrupt:
				sys.exit(0)
		
			try:
				new_mt = [os.path.getmtime(file1), os.path.getmtime(file2)]
			except:
				continue
				
			if new_mt[0] != mt[0] or new_mt[1] != mt[1]:
				mt = new_mt
				fmttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(max(mt)))
				print("File changed, recompiling... [" + fmttime + "]")
				break
	
	while True:
		for path in [file1, file2]:
			if not os.path.exists(path):
				print(f"File not exists: {path}")
				return 1

		vs, ps = None, None
		if file1.endswith(".vs"):
			vs = file1
		elif file1.endswith(".ps"):
			ps = file1
		else:
			print(f"Invalid file extension: {file1}")

		if file2.endswith(".vs"):
			vs = file2
		elif file2.endswith(".ps"):
			ps = file2
		else:
			print(f"Invalid file extension: {file2}")

		if vs is None:
			print("Vertex shader(.vs) not found")
			return 1
		if ps is None:
			print("Pixel shader(.ps) not found")
			return 1
	
		shader = Shader()
		shader.vs_content = open(vs).read()
		shader.ps_content = open(ps).read()
		if err:= validate(vs, "vert"):
			print(Fore.RED + "Vertex shader error:\n", err, Style.RESET_ALL)
			watch_loop()
			continue
		if err:= validate(ps, "frag"):
			print(Fore.RED + "Pixel shader error:\n", err, Style.RESET_ALL)
			watch_loop()
			continue
		
		try:
			shader.update_uniform_list()
		except Exception as e:
			print("Uniform list error:\n", e)
			watch_loop()
			continue
		b = shader.dumps()
		with open(output, "wb") as f:
			f.write(b)

		if not watch:
			return 0
		else:
			print(Fore.GREEN + "OK", Style.RESET_ALL)
			watch_loop()
	