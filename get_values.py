
import mrich
from mrich import print
from pathlib import Path
from gemmi import cif
from typer import Typer

app = Typer()

@app.command()
def get_values(
	source: str,
	model_building: str,
	pattern: str = "*-x????.mmcif",
	refine_subdir_pattern: str = "Refine_*-report",
	key: str = "_refine_ls_shell.number_reflns_R_free",
):
	
	mrich.var("source",source)
	mrich.var("model_building",model_building)
	mrich.var("pattern",pattern)

	source_dir = Path(source)
	model_building_dir = Path(model_building)
	target_dir = source_dir.parent / (source_dir.name + "_fixed")

	mrich.writing(target_dir)
	target_dir.mkdir(exist_ok=True)

	for file in source_dir.glob(pattern):

		# Getting BUSTER report value

		value = 12.34

		model_dir = model_building_dir / (file.name.removesuffix(".mmcif"))

		subdir = sorted(list(model_dir.glob(refine_subdir_pattern)))[-1]

		report_file = subdir / "BUSTER_model.cif"

		try:
			doc = cif.read_file(str(report_file.resolve()))
		except Exception as e:
			mrich.error(e)
			mrich.warning("Skipping")
			continue

		for block in doc:

			col = block.find_values(key)

			if not col:
				continue

			value = col[0]
			break

		# modify the CIF

		mrich.print(file.name, ":", key, value)

		try:
			doc = cif.read_file(str(file.resolve()))
		except Exception as e:
			mrich.error(e)
			mrich.warning("Skipping")
			continue

		for block in doc:

			col = block.find_values(key)

			if not col:
				continue

			col[0] = value

		out_path = target_dir / file.name

		doc.write_file(str(out_path.resolve()))

def main():
	app()

if __name__ == '__main__':
	main()
