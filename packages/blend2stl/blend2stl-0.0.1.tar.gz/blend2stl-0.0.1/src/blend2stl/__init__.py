import bpy
import os
import argparse

def blend2stl(input_folder: str, output_folder: str, scale_factor: float = 1000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    blend_files = [f for f in os.listdir(input_folder) if f.endswith(".blend")]

    for blend_file in blend_files:
        blend_path = os.path.join(input_folder, blend_file)
        bpy.ops.wm.open_mainfile(filepath=blend_path)

        bpy.ops.object.select_all(action='SELECT')
        for obj in bpy.context.selected_objects:
            obj.scale = (scale_factor, scale_factor, scale_factor)

        bpy.ops.object.transform_apply(scale=True)

        stl_output_path = os.path.join(output_folder, blend_file.replace(".blend", ".stl"))
        bpy.ops.export_mesh.stl(filepath=stl_output_path, use_selection=True)
        print(f"Exported: {stl_output_path}")

    print("All files exported!")

def main():
    parser = argparse.ArgumentParser(description="Export .blend files STL with scale")
    parser.add_argument("--input", type=str, default=os.getcwd(), help="Source directory")
    parser.add_argument("--output", type=str, default=os.getcwd(), help="Output directory")
    parser.add_argument("--scale", type=float, default=1000, help="Scale (default 1000)")
    args = parser.parse_args()

    blend2stl(args.input, args.output, args.scale)

if __name__ == "__main__":
    main()
