class FormRegexUtils:
    # base
    token = '^[a-zA-Z0-9]{32}$'
    url = '^(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]$'
    name = '^[\u4e00-\u9fa5_a-zA-Z0-9\-]{1,32}$'
    chunk_IPv4 = '([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
    ip = '^(' + chunk_IPv4 + r'\.){3}' + chunk_IPv4 + r'$'
    file_name = '^[\u4e00-\u9fa5_\- .()（）a-zA-Z0-9]{1,100}$'
    instance_name = '^[\u4e00-\u9fa5_\- .()（）a-zA-Z0-9]{1,100}$'

    # user
    user_id = name
    user_group_id = '^[\u4e00-\u9fa5_a-zA-Z0-9]{1,32}$'
    register_user_id = '^[_a-zA-Z0-9]{1,32}$'
    register_user_name = name
    user_group_name = name
    button_key = name

    group_name = name
    group_name_get = '^[\u4e00-\u9fa5_a-zA-Z0-9]{0,16}$'
    user_name_or_id = '^[\u4e00-\u9fa5_a-zA-Z0-9]{0,32}$'

    user_password = '^[0-9A-Za-z]{5,64}$'
    register_user_password = '^[0-9A-Za-z]{5,64}$'

    user_group_description = name

    # task_manage
    task_id = '^[a-zA-Z0-9]{24}$'
    task_name = name
    task_ai = name

    # scheduler_manage
    scheduler_id = '^[a-zA-Z0-9]{24}$'
    scheduler_task_name = name
    scheduler_create_user = name

    # full_link_monitor
    link_id = '^[a-zA-Z0-9]{24}$'
    link_name = name

    # host_name
    host_name = '^[\u4e00-\u9fa5_a-zA-Z0-9\.\-]{1,100}$'
    target_type = name
    target_class = name
    target_name = '^[\u4e00-\u9fa5_a-zA-Z0-9\-()（） /\.]{1,32}$'
    node_name = name
    index_business = name
    sort_k = name

    # page_config
    create_user = '^[\u4e00-\u9fa5_a-zA-Z0-9\.\-]{1,20}$'
    work_flows = create_user
    desc = '^[\u4e00-\u9fa5_a-zA-Z0-9\.\- ]{1,100}$'

    # mongodb
    _id = '^[a-z0-9]{24}$'
    id_list = '^[a-z0-9]{24}$'
