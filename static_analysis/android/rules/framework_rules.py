
FRAMEWORK_RULES = [
    {
        'desc' : 'Xamarin framework',
        'type': 'regex',
        'match': 'single_regex',
        'regex1': '__md_methods',
        'input_case': 'exact'
    },
    {
        'desc' : 'Cordova framework',
        'type' : 'regex',
        'match' : 'single_regex',
        'regex1' : 'org.apache.cordova',
        'input_case' : 'exact'
    },
    {
        'desc' : 'Flutter framework',
        'type' : 'regex',
        'match' : 'single_regex',
        'regex1' : 'io.flutter',
        'input_case' : 'exact'
    },
    {
        'desc' : 'okHttp library',
        'type' : 'regex',
        'match' : 'regex_or',
        'regex1' : 'okhttp3.',
        'regex2' : 'okhttp2',
        'input_case' : 'exact'
    }
]