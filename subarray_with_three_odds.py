def find_subarrays_with_three_odds(arr):
    n = len(arr)
    result = []

    odd_count_map = {0: [-1]}
    odd_count = 0

    for i in range(n):
        if arr[i] % 2 != 0:
            odd_count += 1

        if (odd_count - 3) in odd_count_map:
            for start_index in odd_count_map[odd_count - 3]:
                result.append(arr[start_index + 1:i + 1])

        if odd_count in odd_count_map:
            odd_count_map[odd_count].append(i)
        else:
            odd_count_map[odd_count] = [i]

    return result


arr = [1, 2, 1, 2, 1, 1, 5]
subarrays = find_subarrays_with_three_odds(arr)
print("Subarrays with  3 odd numbers:")
for subarray in subarrays:
    print(subarray)
