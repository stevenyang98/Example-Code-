def build_time(source_files, transformations, target_file):
    """
    Return milliseconds needed to build the target file, assuming 
    files not dependent on each other can be processed simultaneously.
    Input:      source | list of source file names
            transforms | list of transformations of form
                       | ([input_files], output_file, transform_time)
                target | name of target file to build
   """
    times = {}
    for node in source_files:
        times[node] = 0
    for edge in transformations:
        if edge[1] not in times:
            times[edge[1]] = max([times[node] for node in edge[0]]) + edge[2]
        else:
            current = max([times[node] for node in edge[0]]) + edge[2]
            if current < times[edge[1]]:
                times[edge[1]] = current
        if edge[1] == target_file:
            return times[target_file]




