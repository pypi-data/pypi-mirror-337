def mean(data):
    if not data:
        raise ValueError("The data list is empty.")
    return sum(data) / len(data)


def median(data):
    if not data:
        raise ValueError("The data list is empty.")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]


def mode(data):
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_freq]
    
    return min(modes)  # Return the smallest mode


def multimode(data):
    if not data:
        raise ValueError("The data list is empty.")
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    return [key for key, val in frequency.items() if val == max_freq]



## Used to calculate the mean, median, mode and multimode of a dataset

def Centrality(data):
    # Calculate Mean
    mean = sum(data) / len(data)
    
    # Calculate Median
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        median = sorted_data[n // 2]
    else:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    
    # Calculate Mode and Multimode
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_freq]
    smallest_mode = min(modes)  # Smallest mode
    
    return {
        "Mean": mean,
        "Median": median,
        "Mode": smallest_mode,
        "Multimode": modes
    }
    
    
    
## Mean + Mediaan
def mean_median(data):
    # Calculate Mean
    mean = sum(data) / len(data)
    
    # Calculate Median
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        median = sorted_data[n // 2]
    else:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    
    return {
        "Mean": mean,
        "Median": median
    }


## Calculatin of Mean + Mode


def mean_mode(data):
    # Calculate Mean
    mean = sum(data) / len(data)
    
    # Calculate Mode
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_freq]
    smallest_mode = min(modes)  # Smallest mode
    
    return {
        "Mean": mean,
        "Mode": smallest_mode
    }




# Mean + Multimode
def mean_multimode(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    mean = sum(data) / len(data)
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes in ascending order
    
    return f"Mean: {round(mean, 1)}\nMultiModes: {modes}"




## Median + Mean

def median_mean(data):
    if not data:
        raise ValueError("The data list is empty.")
    mean = sum(data) / len(data)
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2 if n % 2 == 0 else sorted_data[n//2]
    
    return f"Median: {median}\nMean: {mean}"



## Median + Mode
def median_mode(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2 if n % 2 == 0 else sorted_data[n//2]
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes to get the smallest first
    mode = modes[0]  # Always return the smallest mode
    
    return f"Median: {median}\nMode: {mode}"



## median + multimode
def median_multimode(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2 if n % 2 == 0 else sorted_data[n//2]
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes in ascending order
    
    return f"Median: {round(median, 1)}\nMultiModes: {modes}"





## Mode + Mean
def mode_mean(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    mean = sum(data) / len(data)
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes to get the smallest first
    mode = modes[0]  # Always return the smallest mode
    
    return f"Mode: {mode}\nMean: {round(mean, 1)}"



## Mode + Median
def mode_median(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2 if n % 2 == 0 else sorted_data[n//2]
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes to get the smallest first
    mode = modes[0]  # Always return the smallest mode
    
    return f"Mode: {mode}\nMedian: {round(median, 1)}"



#Multimode + mean
def multimode_mean(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    mean = sum(data) / len(data)
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes in ascending order
    
    return f"MultiModes: {modes}\nMean: {round(mean, 1)}"




#Multimode + Median
def multimode_median(data):
    if not data:
        raise ValueError("The data list is empty.")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2 if n % 2 == 0 else sorted_data[n//2]
    
    frequency = {}
    for num in data:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())
    modes = sorted([key for key, val in frequency.items() if val == max_freq])  # Sort modes in ascending order
    
    return f"MultiModes: {modes}\nMedian: {round(median, 1)}"