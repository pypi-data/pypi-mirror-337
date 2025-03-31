from src.fdtdream import FDTDream

sim = FDTDream.new_simulation("test")

sim.add.simulation.fdtd_region(x_min_bc="anti-symmetric", x_max_bc="anti-symmetric",
                               y_min_bc="symmetric", y_max_bc="symmetric")
sim.save()