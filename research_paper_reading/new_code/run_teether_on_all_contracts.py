import json
import func_timeout

from teether.exploit import combined_exploit
from teether.project import Project
from teether.util.utils import denoms

target_addr = 0x1234123412341234123412341234123412341234
shellcode_addr = 0x1000000000000000000000000000000000000000
amount = 1000
amount_check = '+'
initial_storage = {}
initial_balance = 10 * denoms.ether

def hex_encode(d):
    return {k: v.hex() if isinstance(v, bytes) else v for k, v in d.items()}

def check(code_path):
    print(code_path)
    with open(code_path) as infile:
        inbuffer = infile.read().rstrip()
    code = bytes.fromhex(inbuffer)
    p = Project(code)
    savefilebase = code_path.split('/')[-1]
    result = None
    try:
        result = func_timeout.func_timeout(1200.0, combined_exploit, args=[p, target_addr, shellcode_addr, amount, amount_check,
                                initial_storage, initial_balance])
    except func_timeout.FunctionTimedOut:
        print(f'{savefilebase} exceeded time limit of 20 mins for detecting exploits')
        return
    if result:

        call, r, model = result

        print(model)

        with open('%s.exploit.json' % savefilebase, 'w') as f:
            json.dump({'paths': [{'index': i, 'path': [ins for ins in res.state.trace if
                                                    ins in p.cfg.bb_addrs or ins == res.state.trace[-1]]} for
                                i, res in enumerate(r.results)],
                    'calls': [{'index': i, 'call': hex_encode(c)} for i, c in enumerate(call)]}, f)

        for i, res in enumerate(r.results):
            print('%d: %s' % (
                i, '->'.join('%x' % i for i in res.state.trace if i in p.cfg.bb_addrs or i == res.state.trace[-1])))
        print(call)
        print()
        for c in call:
            if c['caller'] == c['origin']:
                print('eth.sendTransaction({from:"0x%040x", data:"0x%s", to:"0x4000000000000000000000000000000000000000"%s, gasPrice:0})' % (
                    c['origin'], c.get('payload', b'').hex(),
                    ", value:%d" % c['value'] if c.get('value', 0) else ''))
            else:
                print('eth.sendTransaction({from:"0x%040x", data:"0x%s", to:"0x%040x"%s, gasPrice:0})' % (
                    c['origin'], c.get('payload', b'').hex(), c['caller'],
                    ", value:%d" % c['value'] if c.get('value', 0) else ''))

def main():
    for i in range(1, 1000):
        check(f'tests/data/test{i}.contract.code')

if __name__ == '__main__':
    main()