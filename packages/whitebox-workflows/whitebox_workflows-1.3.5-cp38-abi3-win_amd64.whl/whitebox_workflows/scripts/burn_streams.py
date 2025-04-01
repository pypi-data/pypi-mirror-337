import time
from whitebox_workflows import Raster, Vector, WbEnvironmentBase
from .utils import print_tool_header

def burn_streams(wbe: WbEnvironmentBase, dem: Raster, streams: Vector, decrement_value: float = 5.0, gradient_distance: int = 5) -> Raster:
    start = time.time()
    try:
        reset_verbose = wbe.verbose
        if wbe.verbose:
            print_tool_header("burn_streams")
            print("\nPerforming operation...")

        wbe.verbose = False # suppress the output from each of the workflow components

        grid_res = (dem.configs.resolution_x + dem.configs.resolution_x) / 2.0
        
        # Convert the streams vector to a raster
        streams_raster = wbe.rasterize_streams(
            streams=streams, 
            base_raster=dem, 
            zero_background=True, 
            use_feature_id=False
        )
        
        print('Burning streams...')
        if gradient_distance <= 0.0: 
            # Perform a straightforward elevation decrement on stream cells only
            burned_dem = dem - (streams_raster * decrement_value)
        else:
            # Decrement stream cells by the decrement_value and then apply a gradient away from the streams

            # First calculate the distance away from streams
            dist = wbe.euclidean_distance(streams_raster)

            # Now covert that value into a decrement value
            dist_threshold = gradient_distance * grid_res # Put the gradient distance in map units rather than grid cells

            # This is where the elevation decrement and gradient are added
            burned_dem = dem + (((dist - dist_threshold) / dist_threshold).min(0.0)) * decrement_value

        wbe.verbose = reset_verbose

        return burned_dem
    except Exception as e:
        print("The error raised is: ", e)
    finally:
        end = time.time()
        print(f'Elapsed time: {end-start}s')