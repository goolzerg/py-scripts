import hvac, os, sys, json, getopt

client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
args = sys.argv
argument_list = args[1:]
short_options = "hm:o:i:r:"
long_options = ["help", "method=", "output=", "input=", "root="]
get_args_pairs = [['--root', '-r'], ['--method', '-m'], ['--output', '-o']]
put_args_pairs = [['--root', '-r'], ['--method', '-m'], ['--input', '-i']]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for current_argument, current_value in arguments:
    if current_argument in ("-i", "--input"):
        input = current_value

for current_argument, current_value in arguments:
    if current_argument in ("-o", "--output"):
        output = current_value

for current_argument, current_value in arguments:
    if current_argument in ("-r", "--root"):
        root = current_value

def parse_variable_names():
    try:
        with open(input) as f:
            data = json.load(f)
    except IndexError:
        print('ERROR: File not found')

    def strkeys(data):
        if isinstance(data, dict):
            for k, v in data.items():
                for item in strkeys(v):
                    yield f'{k}__{item}' if item else k
        elif isinstance(data, list):
            for i, v in enumerate(data):
                for item in strkeys(v):
                    yield f'{i}__{item}' if item else str(i)
        else:
            yield None

    variables = list()
    for var in strkeys(data):
        variables.append(var)
    return variables


def vault_get_variables(environment, write_to_file, root):
    if write_to_file is True:
        envfile = open(output, 'w')
    try:
        secrets_under_path = client.secrets.kv.v2.list_secrets(mount_point=root,
                                                               path=os.environ['SERVICE_NAME'] + '/' + environment)
        secrets_keys = secrets_under_path['data']['keys']
        variables = list()
        for key in secrets_keys:
            secret = (client.read(
                root + '/data/' + os.environ['SERVICE_NAME'] + '/' + os.environ['ENV_VAULT'] + '/' + key))
            try:
                for key in secret['data']['data']:
                    variables.append(key)
                    if write_to_file is True:
                        envfile.write(key + '=' + secret['data']['data'][key] + '\n')
                    else:
                        continue
            except TypeError:
                continue
        if write_to_file is True:
            envfile.close()
            print('Successfully red variables from "' + root + '/' + os.environ['SERVICE_NAME'] + '/' +
                  os.environ[
                      'ENV_VAULT'] + '"')
            print('Variables have been written in ' + output)
        return variables
    except hvac.exceptions.InvalidPath:
        if write_to_file is not False:
            print(
                'WARN: Path not found "' + root + '/' + os.environ['SERVICE_NAME'] + '/' + os.environ[
                    'ENV_VAULT'] + '"')


def vault_put_variables(variables, root):
    environment = ['test', 'stage', 'prod']
    try:
        for env in environment:
            env_variables = variables.copy()
            vars_exists = vault_get_variables(env, write_to_file=False, root=root)
            try:
                for var in vars_exists:
                    if var in env_variables:
                        env_variables.remove(var)
            except TypeError:
                print('WARN: List of already existed variables is empty. Possible, path is not exists.')
            for var in env_variables:
                var_kv = {var: ''}
                client.secrets.kv.v2.create_or_update_secret(mount_point=root,
                                                             path=os.environ['SERVICE_NAME'] + '/' + env + '/' + var,
                                                             secret=var_kv)
            print('Variables added to ' + env + ' = ' + str(len(env_variables)) + '\nList of added vars: ' + str(
                env_variables) + '\n')
    except hvac.exceptions.InvalidPath:
        print(
            'WARN: Path not found "' + root + '/' + os.environ['SERVICE_NAME'] + '/' + os.environ[
                'ENV_VAULT'] + '"')


def check_args_existence(passed_arguments, args_pair):
    if args_pair[0] in (item for subtuple in passed_arguments for item in subtuple) or args_pair[1] in (
            item for subtuple in passed_arguments for item in subtuple):
        pass
    else:
        print('WARN: You should specify "' + args_pair[0] + '" or "' + args_pair[1] + '" parameter')
        exit(1)

def check_method():
    for current_argument, current_value in arguments:
        if current_argument in ("-m", "--method"):
            if current_value.lower() == 'put':
                for pair in put_args_pairs:
                    check_args_existence(arguments, pair)
                vault_put_variables(parse_variable_names(), root)
            elif current_value.lower() == 'get':
                for pair in get_args_pairs:
                    check_args_existence(arguments, pair)
                print('Getting variables')
                vault_get_variables(os.environ['ENV_VAULT'], write_to_file=True, root=root)
            else:
                print('ERROR: Unknown method: ' + current_value)
check_method()

