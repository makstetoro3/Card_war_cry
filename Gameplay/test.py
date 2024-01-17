def tesr_id(func):
    def _test_id():
        if id != -1:
            func(-1)
    return _test_id


@tesr_id
def hell(id):
    print('hi')


id = -1
hell()
print('bye')
