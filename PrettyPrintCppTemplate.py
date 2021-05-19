import sublime
import sublime_plugin


class PrettyPrintCppTemplateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        for region in regions:
            selection, selected_entire_file = PrettyPrintCppTemplateCommand.get_selection_from_region(
                region=region, regions_length=len(regions), view=self.view
            )
            if selection is None:
                continue

            selection_text = self.view.substr(selection)
            self.view.replace(edit, selection, PrettyPrintCppTemplateCommand.replace_text(selection_text))


    @staticmethod
    def replace_text(text):
        stack = []
        tokens = ["<",">","(",")","{","}"]
        depth_changes = [+1,-1,+1,-1,+1,-1]
        text_tokens = []

        last_token_end = None
        for i in range(len(text)):
            for token,depth_change in zip(tokens,depth_changes):
                if text[i:i+len(token)] == token:
                    if last_token_end is not None:
                        text_token = text[last_token_end:i].strip("\n\r ")
                        if len(text_token) > 0:
                            text_tokens.append((0,text_token))
                    text_tokens.append((depth_change,token))
                    last_token_end = i+len(token)
        level = 0
        lines = []
        indent = "    "
        for depth_change,token in text_tokens:
            if depth_change < 0:
                level = level+depth_change
            lines.append(indent*level + token)
            if depth_change > 0:
                level = level+depth_change

        return "\n".join(lines)

    @staticmethod
    def get_selection_from_region(
        region: sublime.Region, regions_length: int, view: sublime.View
    ) -> sublime.Region:
        selected_entire_file = False
        if region.empty() and regions_length > 1:
            return None, None
        elif region.empty() and s.get("use_entire_file_if_no_selection", True):
            selection = sublime.Region(0, view.size())
            selected_entire_file = True
        else:
            selection = region
        return selection, selected_entire_file
        