import argparse
import yaml


if __name__ == '__main__':
    cmd_args = argparse.ArgumentParser()
    cmd_args.add_argument(
        '--sample',
        dest='sample',
        type=str,
        required=True
    )
    cmd_args.add_argument(
        '--nameurl',
        dest='nameurl',
        type=str,
        required=True
    )
    cmd_args.add_argument(
        '--url',
        dest='url',
        type=str,
        required=True
    )
    cmd_args.add_argument(
        '--pattern',
        dest='pattern',
        type=str
    )
    cmd_args.add_argument(
        '--nameservice',
        dest='nameservice',
        type=str,
        required=True
    )
    cmd_args.add_argument(
        '--kafkaurl',
        dest='kafkaurl',
        type=str,
        required=True
    )
    cmd_args.add_argument(
        '--kafkaport',
        dest='kafkaport',
        type=int,
        required=True
    )
    cmd_args.add_argument(
        '--kafkatopic',
        dest='kafkatopic',
        type=str
    )
    args = cmd_args.parse_args()
    config = {
        'Metrics endpoint': {},
        'Monitored web sites': {}
    }
    config_monitored = {
        'url': '',
        'expected pattern': '',
        'request sleep': 10
    }
    config_metrics = {
        'Kafka': {
            'host': '',
            'port': None,
            'topic': ''
        }
    }

    config['Monitored web sites'][args.nameurl] = config_monitored
    config['Monitored web sites'][args.nameurl]['url'] = args.url
    config['Monitored web sites'][args.nameurl]['expected pattern'] = args.pattern

    config['Metrics endpoint'][args.nameservice] = config_metrics
    config['Metrics endpoint'][args.nameservice]['Kafka']['host'] = args.kafkaurl
    config['Metrics endpoint'][args.nameservice]['Kafka']['port'] = args.kafkaport
    config['Metrics endpoint'][args.nameservice]['Kafka']['topic'] = args.kafkatopic
    with open(args.sample.replace('.example', ''), 'w+') as f:
        yaml.safe_dump(config, f)
