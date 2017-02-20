'''
    Usage:
        python remove_from_env.py $PATH $TO_BE_REMOVED
    returns $PATH without paths starting with $TO_BE_REMOVED
'''
import sys

ENV = sys.argv[1]
REMOVE = sys.argv[2]
if not REMOVE:
    sys.exit()

new_path = []
# print('ENV', ENV)
for path in ENV.split(':'):
    if path.startswith(REMOVE):
        continue
    new_path.append(path)
print ':'.join(new_path)
