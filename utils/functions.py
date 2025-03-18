def create_shikigami(member_info: dict, shikigami_collection: tuple, spirits_collection: tuple):
    shikigami_info = member_info.get('shikigami_info')
    shikigami_spirit = member_info.get('shikigami_spirit')

    # extract shikigami class
    shikigami_dict = {cls.__name__.lower(): cls for cls in shikigami_collection}
    current_shikigami = shikigami_dict.get(shikigami_info.get['name'], None)
    if current_shikigami:
        shikigami = current_shikigami(**shikigami_info)
    else:
        raise ValueError(f'无法找到式神{shikigami_info.get["name"]}的信息')

    # add spirit to shikigami
    shikigami.add_spirit(spirit_name=shikigami_spirit,
                         spirits_collection=spirits_collection)

    return shikigami
