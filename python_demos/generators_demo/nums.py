""" generator demo with simple numbers """


# nums = [1,2,3,4,5]

# print(nums)
# print(type(nums))

# print(range(5))
# print(type(range(5)))

# for num in nums:

# def get_nums():
#     return [0,1,2,3,4]

# def get_nums():
#     print("inside get_nums")
#     yield 0
#     print("inside get_nums")
#     yield 1
#     print("inside get_nums")
#     yield 2
#     print("inside get_nums")
#     yield 3
#     print("inside get_nums")
#     yield 4


nums = [1,2,3,4,5]

double_nums = map(lambda x: x * 2, nums)

print(list(double_nums))

double_nums2 = [ num * 2 for num in nums ]

print(double_nums2)


# for num in get_nums():
#     print("inside for loop")
#     print(num)


# counter = 0

# while counter < 5:
#     print(counter)
#     counter += 1
