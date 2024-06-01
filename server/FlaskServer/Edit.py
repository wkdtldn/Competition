def edit(dbList):
    _dictionaryList_ = []
    for trash in dbList:
        container = {"name" : trash[0] ,"description" : trash[1], "disposal_method" : trash[2]}
        _dictionaryList_.append(container)
    return _dictionaryList_
