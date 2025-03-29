from gm3dh5.file import GM3DResultFileReader

grains_file = "./sample_S_undeformed_6_grain_center_slice.h5"
tesr_file = "Al.tesr"

with GM3DResultFileReader(grains_file) as f:
    f.export(tesr_file)