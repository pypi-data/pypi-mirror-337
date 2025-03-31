import defix_package_logger


def main():
    defix_package_logger.initialize({
        'name': 'test-service'
    })

    defix_package_logger.get_logger().info('Logging', extra={
        'msg_code': 'CRITICAL_ERROR'
    } | {'xid': '-'})


if __name__ == "__main__":
    main()
