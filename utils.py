def print_results(overlaped_black_pixels, microscope_black_pixels, start_time, end_time):
    # Print results
    print('Overlap: ' + str((overlaped_black_pixels /
        microscope_black_pixels)*100)[:5] + '%')
    if (overlaped_black_pixels/microscope_black_pixels)*100 > 10:
        print('Parasite have cancer')
    else:
        print('Parasite do not have cancer')

    # Print time
    print('Execution time: ' + str(end_time - start_time)[:5] + 's')