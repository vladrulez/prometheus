#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Nagios/Icinga check for Prometheus targets

import requests
import sys
import argparse

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Prometheus targets status check')
        parser.add_argument('--url', help='Prometheus server url like DOMAIN.COM/prometheus/api/v1/targets', nargs='?', required=True)
        args = parser.parse_args()
    except Exception as ex:
        sys.stderr.write(str(ex))
        sys.exit(3)
    
    if not args.url:
        sys.stderr.write('\n--url option are required and can not be empty\n\n')
        parser.print_help()
        sys.exit(3)
    else:
        try:
            r = requests.get(url=args.url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
      
        result = r.json()
        input_data = result['data']['activeTargets']
        output_data = []

        for i in input_data:
            if i['health'] == 'down' or i['health'] != 'up':
                output_data.append(i['scrapeUrl'])

        if output_data:
            output_str = 'Targets down: '
            for i in output_data:
                output_str = output_str + i
                output_str = output_str + ' '
            output_str = output_str + ' PROMETHEUS CRITICAL \n'
            sys.stderr.write(output_str)
            sys.exit(2)
        else:
            sys.stderr.write('PROMETHEUS OK\n')
            sys.exit(0)
