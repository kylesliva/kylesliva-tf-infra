#! /usr/bin/env python3

# pulled from https://filip-prochazka.com/blog/importing-your-existing-aws-route53-records-into-terraform 
import json
import re
from pathlib import Path
from typing import Any, Dict, List

project_dir = Path('/Users/kylesliva/repos/kylesliva-tf-infra')

domain = 'kylesliva.me'
domain_snake = domain.replace('.', '_')
input_file = project_dir / f'route53_{domain_snake}.json'
tf_output_file = project_dir / f'route53_{domain_snake}_records.tf'

with open(input_file) as f:
    existing_records = json.load(f)


def rec_contains(resource_records: List[Dict[str, Any]], needle: str) -> bool:
    for item in resource_records:
        if needle in item['Value']:
            return True
    return False


with open(tf_output_file, mode='w', encoding='utf-8') as out:
    for record_set in existing_records['ResourceRecordSets']:
        r_type = record_set.get('Type')
        if r_type == 'NS' or r_type == 'SOA':
            continue

        r_name: str = record_set.get('Name')
        r_ttl: int = record_set.get('TTL') or 1800
        r_records = record_set.get('ResourceRecords')
        r_alias = record_set.get('AliasTarget')

        if r_alias:
            r_hosted_zone_id = r_alias.get('HostedZoneId')
            r_dsn_name = r_alias.get('DNSName')

            if '.elb.amazonaws.' in r_dsn_name:
                resource_name = 'aws_elb_' + r_name.replace(f'{domain}.', '')
            else:
                resource_name = r_name.replace(f'{domain}.', '')

            resource_name = re.compile(r'[_.-]+').sub('_', domain_snake + '_' + resource_name + '_' + r_type).strip('_')

            out.write(f'resource "aws_route53_record" "{resource_name}" ' + "{\n")
            out.write(f'  zone_id = aws_route53_zone.{domain_snake}.zone_id' + "\n")
            out.write(f'  name = "{r_name}"' + "\n")
            out.write(f'  type = "{r_type}"' + "\n")
            out.write('  alias {' + "\n")
            out.write(f'    name = "{r_dsn_name}"' + "\n")
            out.write(f'    zone_id = "{r_hosted_zone_id}"' + "\n")
            out.write(f'    evaluate_target_health = false' + "\n")
            out.write('  }' + "\n")
            out.write(f'  allow_overwrite = true' + "\n")
            out.write('}' + "\n")

        else:
            if rec_contains(r_records, 'dkim.amazonses'):
                resource_name = 'amazonses_dkim_' + r_name.replace(f'{domain}.', '').replace('_domainkey', '')
            elif rec_contains(r_records, 'acm-validations'):
                resource_name = 'aws_acm_' + r_name.replace(f'_domainkey.{domain}.', '')
            else:
                resource_name = r_name.replace(f'{domain}.', '')

            resource_name = re.compile(r'[_.-]+').sub('_', domain_snake + '_' + resource_name + '_' + r_type).strip('_')

            out.write(f'resource "aws_route53_record" "{resource_name}" ' + "{\n")
            out.write(f'  zone_id = aws_route53_zone.{domain_snake}.zone_id' + "\n")
            out.write(f'  name = "{r_name}"' + "\n")
            out.write(f'  type = "{r_type}"' + "\n")
            out.write(f'  ttl = {r_ttl}' + "\n")
            out.write(f'  records = [' + "\n")
            for record_item in r_records:
                r_i_val = record_item["Value"].strip('"')
                out.write(f'    "{r_i_val}",' + "\n")
            out.write(f'  ]' + "\n")
            out.write(f'  allow_overwrite = true' + "\n")
            out.write('}' + "\n")

        out.write("\n")