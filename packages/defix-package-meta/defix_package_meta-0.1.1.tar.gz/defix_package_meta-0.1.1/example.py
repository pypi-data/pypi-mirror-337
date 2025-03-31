import defix_package_meta


def main():
    defix_package_meta.initialize({'name': 'example'})
    print(defix_package_meta.generate_meta())


if __name__ == '__main__':
    main()
