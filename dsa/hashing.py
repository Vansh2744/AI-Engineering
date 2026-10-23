#-----------------------Hashing using List--------------------------

def list_hash(arr1:list[int], arr2:list[int])->None:
    hash_list = [0]*11  #Bcz arr1 have values 1 to 10 so indexing starts from 0 to 10

    for num in arr1:
        hash_list[num] += 1

    for num in arr2:
        if num in arr1:
            print(hash_list[num])
        else:
            print(0)

arr1 = [2,3,4,5,5,6,3,3,2,2,8,10,10,4,5,4,4,5,6,7,7,8]
arr2 = [2,3,4,5,60,6,70,7,8,9,10,11,20,30,40]

# list_hash(arr1, arr2)

#----------------------Hashing using Dictionary---------------------------
def dict_hash(arr:list[int])->dict:
    hash_dict = {}
    for num in arr:
        hash_dict[num] = hash_dict.get(num, 0) + 1

    return hash_dict

arr = [2,3,4,5,5,6,3,3,2,2,8,10,10,4,5,4,4,5,6,7,7,8]

print(dict_hash(arr))