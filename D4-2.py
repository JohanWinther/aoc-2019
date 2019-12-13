pass_min = 357253
pass_max = 892942

def pass_to_array(p):
    return [p//100000, p//10000 % 10,
            p // 1000 % 10, p // 100 % 10,
            p // 10 % 10, p % 10,
            ]
def valid_pass(p):
    if p < pass_min or p > pass_max:
        return False
    
    a = pass_to_array(p)
    inc = True
    groups = []
    for i in range(len(a)-1):
        if a[i] == a[i + 1]:
            groups.append(a[i])
        if a[i] > a[i + 1]:
            inc = False
    adj = [groups.count(n) for n in set(groups)]
    if 1 not in adj or not inc:
        return False

    return True

passwords = range(pass_min,pass_max)
valid_passwords = list(filter(valid_pass, passwords))
print(valid_passwords)
print(len(valid_passwords))
