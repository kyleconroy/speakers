from django.test.runner import DiscoverRunner


class RoadRunner(DiscoverRunner):
    """ A test runner to test without database creation/deletion """
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
