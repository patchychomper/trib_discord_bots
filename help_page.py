from string import Template


class HelpCreate:
    """
    Create a help page for display upon given command (such as !help).
    """
    def __init__(self, data, cmd_char='/'):
        self.data = data
        self.cmd_char = cmd_char
        self.entries_info = self._entries_create()
        self.entries_split = self._help_split(len(self.entries_info)+1, 2)
        self.final_entries = self._entry_gather(self.entries_split, self.entries_info)

        self.help_info = self._help_create()
        self.help_split = self._help_split(len(self.help_info)+1, 1)
        self.final_help = self._entry_gather(self.help_split, self.help_info)

    def _entries_create(self):
        """
        Format the text.  Maybe just use a template.
        :return:
        """
        help_info = []
        help_tmpl = Template('**$long_name** [$short_name]:\t$question')
        for key, val in self.data.items():
            help_info.append(help_tmpl.substitute(val))
        return help_info

    def _help_create(self):
        """
        Format the text.  Maybe just use a template.
        :return:
        """
        help_info = []
        help_tmpl = Template('**' + self.cmd_char + '$command**:\t$descrip')
        for key, val in self._help_page().items():
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

    def _entry_gather(self, split, data):
        """
        Discord has a limit of 2000 characters per response, so we need to split help screen in to multiple reponses.
        :return:
        """
        new_help = []
        for entry in split:
            to_add = '\n'.join(data[entry[0]:entry[-1]])
            new_help.append(to_add)
        return new_help

    def _help_page(self):
        """
        Provide basic help page that lists commands.
        :return:
        """
        content = {'help': {'command': 'help', 'descrip': 'This help page.'},
                   'entries': {'command': 'entries', 'descrip': 'List all available FAQs.'}
        }
        return content