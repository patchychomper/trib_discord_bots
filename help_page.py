from string import Template


class HelpCreate:
    """
    Create a help page for display upon given command (such as !help).
    """
    def __init__(self, data):
        self.data = data
        self.help_info = self._help_create()
        self.help_split = self._help_split(len(self.help_info)+1, 2)
        self.final_help = self._entry_gather()

    def _help_create(self):
        """
        Format the text.  Maybe just use a template.
        :return:
        """
        help_info = []
        help_tmpl = Template('**$long_name** [$short_name]:\t$question')
        for key, val in self.data.items():
            help_info.append(help_tmpl.substitute(val))
        return help_info

    @staticmethod
    def _help_split(a, n):
        """
        Split in to lists based on total number of entries an number of groups we want.
        Stolen from:
        https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
        :return:
        """
        a = range(a)
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def _entry_gather(self):
        """
        Discord has a limit of 2000 characters per response, so we need to split help screen in to multiple reponses.
        :return:
        """
        new_help = []
        for entry in self.help_split:
            to_add = '\n'.join(self.help_info[entry[0]:entry[-1]])
            new_help.append(to_add)
        return new_help
