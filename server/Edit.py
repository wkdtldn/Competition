def edit(dbList):
    _dictionaryList_ = []
    for trash in dbList:
        container = {"id" : trash[0],"name" : trash[1] ,"description" : trash[2], "disposal_method" : trash[3], "image" : trash[4]}
        _dictionaryList_.append(container)
    return _dictionaryList_
