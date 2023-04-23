def callback_parsing(callback_string: str, number_id: int):
    callback_list = callback_string.split('\n')
    agent_dict = {'last_user': number_id}
    for i in range(0, len(callback_list) - 1):
        if ': ' in callback_list[i]:
            agent_dict[callback_list[i].split(':')[0]] = callback_list[i].split(':')[1]
    return (agent_dict)
