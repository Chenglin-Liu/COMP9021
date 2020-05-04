import re
import itertools
from copy import deepcopy


class DiffCommandsError(Exception):
    pass


class DiffCommands:

    def __init__(self, file_name):
        self.file_name = file_name
        self.commands = []

        with open(self.file_name, 'r') as file:
            for line in file:
                # Check if the line is empty
                if line.isspace():
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')

                left_position, operation, right_position = self.extract_command(line)
                result = self.command_checker(left_position, operation[0], right_position, self.commands)

                if result == 0:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                self.commands.append(line.strip())

    def __str__(self):
        output_commands = [command.strip() for command in self.commands]
        return '\n'.join(output_commands)

    def extract_command(self, command):
        """
        Extract operation position and operation from command
        Return form: list
        """
        # Get string before and behind the word
        left = re.findall(r'(\d+,\d+|\d+)\w\d', command)
        right = re.findall(r'\d\w(\d+,\d+|\d+)$', command)
        left_position = []
        right_position = []
        # Extract position of operation
        if left:
            left_position = left[0].split(',')
        if right:
            right_position = right[0].split(',')
        # Extract operation
        operation = re.findall(r'\d(\w)\d', command)

        return left_position, operation, right_position

    def command_checker(self, left_position, operation, right_position, commands):
        if left_position and right_position and operation:
            # Operation is 'a' or 'c' or 'd'
            if operation not in ['a', 'c', 'd']:
                return 0
            # Only 1 number(= left position - 1) behind 'd'
            if operation == 'd':
                if (len(right_position) > 1) or \
                        (int(left_position[0]) == 1 and int(right_position[0]) != int(left_position[0]) - 1):
                    return 0
            # Only 1 number before 'a'
            if operation == 'a':
                if len(left_position) > 1:
                    return 0
            if operation == 'c':
                if len(commands) != 0:
                    last_left_position, last_operation, last_right_position = self.extract_command(commands[-1])
                    left_gap = int(left_position[0]) - int(last_left_position[-1])
                    right_gap = int(right_position[0]) - int(last_right_position[-1])
                    # Number before c should > last left position[-1] + 1  & left_gap = right_gap
                    if (int(left_position[0]) - 1 <= int(last_left_position[-1])) or (left_gap != right_gap):
                        return 0
            return 1
        else:
            return 0


class OriginalNewFiles:
    def __init__(self, file_1, file_2):
        self.file_1_content = []
        self.file_2_content = []

        with open(file_1, 'r') as file1:
            for line_1 in file1:
                self.file_1_content.append(line_1)

        with open(file_2, 'r') as file2:
            for line_2 in file2:
                self.file_2_content.append(line_2)

    def add_content(self, left_position, right_position, adjuster, modified_file):
        """
        Add content from file2 to file 1
        e.g. 3a2: ADD line2 in FILE2 to FILE1 at index = 3
        """
        if len(right_position) == 2:
            modified_file = modified_file[:int(left_position[0]) + adjuster] + \
                            self.file_2_content[int(right_position[0]) - 1: int(right_position[1])] + \
                            modified_file[int(left_position[0]) + adjuster:]
            adjuster += int(right_position[1]) - int(right_position[0]) + 1
        else:
            modified_file.insert(int(left_position[0]) + adjuster, self.file_2_content[int(right_position[0]) - 1])
            adjuster += 1

        return adjuster, modified_file

    def delete_content(self, left_position, adjuster, modified_file):
        """
        Delete content in file1 and sync up with file2
        e.g. 1,2d0: DELETE line1 to line2 in FILE1 and Sync up with content BEFORE(contains) line 0 in FILE2
        """
        if len(left_position) == 2:
            del modified_file[int(left_position[0]) - 1 + adjuster: int(left_position[1]) + adjuster]
            adjuster -= int(left_position[1]) - int(left_position[0]) + 1
        else:
            del modified_file[int(left_position[0]) - 1 + adjuster]
            adjuster -= 1

        return adjuster, modified_file

    def operate(self, left_position, operation, right_position, adjuster, modified_file):
        if operation[0] == 'a':
            adjuster, modified_file = self.add_content(left_position, right_position, adjuster, modified_file)

        elif operation[0] == 'd':
            adjuster, modified_file = self.delete_content(left_position, adjuster, modified_file)

        elif operation[0] == 'c':
            # Delete the element(s) in file1
            adjuster_1, modified_file = self.delete_content(left_position, adjuster, modified_file)

            # Insert element(s) from file2
            adjuster_2, modified_file = self.add_content([int(left_position[0]) - 1], right_position, adjuster, modified_file)

            adjuster = adjuster_1 + adjuster_2 - adjuster

        return adjuster, modified_file

    def _output_add(self, right_position):
        if len(right_position) == 2:
            for line_number in range(int(right_position[0]) - 1, int(right_position[1])):
                print('> ' + self.file_2_content[line_number], end='')
        else:
            print('> ' + self.file_2_content[int(right_position[0]) - 1], end='')

    def _output_delete(self, left_position):
        if len(left_position) == 2:
            for line_number in range(int(left_position[0]) - 1, int(left_position[1])):
                print('< ' + self.file_1_content[line_number], end='')
        else:
            print('< ' + self.file_1_content[int(left_position[0]) - 1], end='')

    def _change_line_to_ellipsis(self, file, line, adjuster):
        if len(line) == 2:
            change_line_num = int(line[1]) - int(line[0]) + 1
        else:
            change_line_num = 1

        file = file[: int(line[0]) - 1 + adjuster] + ['...\n'] + file[int(line[0]) + adjuster + change_line_num - 1:]
        adjuster = adjuster - change_line_num + 1

        return file, adjuster

    def _output_unmodified_file(self, diff_commands, file, file_type):
        """
        Delete line(s) in file (original(file_type = 1) / new(file_type = 2)) and print '...'
        """
        adjuster = 0
        for command in diff_commands.commands:
            left_position, operation, right_position = DiffCommands.extract_command(diff_commands, command)

            if operation[0] == 'a' and file_type == 2:
                file, adjuster = self._change_line_to_ellipsis(file, right_position, adjuster)

            if operation[0] == 'd' and file_type == 1:
                file, adjuster = self._change_line_to_ellipsis(file, left_position, adjuster)

            if operation[0] == 'c':
                if file_type == 1:
                    file, adjuster = self._change_line_to_ellipsis(file, left_position, adjuster)
                elif file_type == 2:
                    file, adjuster = self._change_line_to_ellipsis(file, right_position, adjuster)

        return file

    def get_lcs(self, file1, file2, dict):
        """
        Calculate Longest common sequence
        file1 and file2 are list
        """
        len1 = len(file1)
        len2 = len(file2)
        if f'file1[:{len1}]&file2[:{len2}]' in dict.keys():
            return dict[f'file1[:{len1}]&file2[:{len2}]']

        if len1 == 0 or len2 == 0:
            dict[f'file1[:{len1}]&file2[:{len2}]'] = []
            return []

        elif file1[-1] == file2[-1]:
            dict[f'file1[:{len1}]&file2[:{len2}]'] = self.get_lcs(file1[:-1], file2[:-1], dict) + [file1[-1]]
            return self.get_lcs(file1[:-1], file2[:-1], dict) + [file1[-1]]

        elif file1[-1] != file2[-1]:
            path_1 = self.get_lcs(file1, file2[:-1], dict)
            path_2 = self.get_lcs(file1[:-1], file2, dict)

            if len(path_1) > len(path_2):
                dict[f'file1[:{len1}]&file2[:{len2}]'] = path_1
                return path_1
            elif len(path_1) == len(path_2) and path_1 != path_2:
                return [path_1, path_2]
            else:
                dict[f'file1[:{len1}]&file2[:{len2}]'] = path_2
                return path_2

    def find_all_index(self, file, pattern):
        all_index = []
        for i in range(file.index(pattern), len(file)):
            if file[i] == pattern:
                all_index.append(i)

        return all_index

    def get_possible_lcs_index(self, all_combination):
        possible_combination = list(itertools.product(*all_combination))
        for combination in possible_combination[:]:
            result = all(combination[i] <= combination[i + 1] for i in range(len(combination) - 1))
            if not result:
                possible_combination.remove(combination)
        return possible_combination

    def get_one_possible_diff(self, lcs_file1, lcs_file2, file1, file2):
        """
        Get possible diff command from two lcs indices(file1 and file2)
        give command according to the gap (end - start) between two Common Sequences
        0. do nothing. When gap 1 = and gap2 = 1
        1. ADD('a'). When gap1 = 1 and gap2 != 1
        2. DELETE('d'). When gap1 != 1 and gap2 = 1
        3. CHANGE('c'). When gap1 != 1 and gap2 != 1
        """
        # Normalize LCS
        lcs_file1 = [-1] + list(lcs_file1) + [len(file1)]
        lcs_file2 = [-1] + list(lcs_file2) + [len(file2)]
        possible_diff = []
        # Initialize start and end
        start1 = lcs_file1[0]
        start2 = lcs_file2[0]
        end1 = lcs_file1[1]
        end2 = lcs_file2[1]
        index = 1  # Index of the end

        while index < len(lcs_file1):
            gap1 = end1 - start1
            gap2 = end2 - start2

            # Case 0: Do Nothing
            if gap1 == 1 and gap2 == 1:
                command = []
            # Case 1: ADD
            elif gap1 == 1 and gap2 != 1:
                if gap2 == 2:
                    command = f'{start1 + 1}a{start2 + 2}'
                else:
                    command = f'{start1 + 1}a{start2 + 2},{end2}'
            # Case 2: DELETE
            elif gap1 != 1 and gap2 == 1:
                if gap1 == 2:
                    command = f'{start1 + 2}d{end2}'
                else:
                    command = f'{start1 + 2},{end1}d{end2}'
            # Case 3:CHANGE
            else:
                if gap1 > 2:
                    if gap2 > 2:
                        command = f'{start1 + 2},{end1}c{start2 + 2},{end2}'
                    else:
                        command = f'{start1 + 2},{end1}c{start2 + 2}'
                else:
                    if gap2 > 2:
                        command = f'{start1 + 2}c{start2 + 2},{end2}'
                    else:
                        command = f'{start1 + 2}c{start2 + 2}'

            if command:
                possible_diff.append(command)

            # Update start, end, index
            index += 1
            start1 = end1
            start2 = end2

            if index < len(lcs_file1):
                end1 = lcs_file1[index]
                end2 = lcs_file2[index]
            else:
                pass

        return possible_diff

    def is_a_possible_diff(self, diff_commands):
        # diff_commands is an object of DiffCommands
        modified_file = deepcopy(self.file_1_content)
        adjuster = 0  # Adjust the line to operate after 'a' or 'd'
        for command in diff_commands.commands:
            left_position, operation, right_position = DiffCommands.extract_command(diff_commands, command)
            if int(left_position[-1]) > len(modified_file) or int(right_position[-1]) > len(self.file_2_content):
                return False

            adjuster, modified_file = self.operate(left_position, operation, right_position, adjuster, modified_file)

        if modified_file == self.file_2_content:
            return True
        else:
            return False

    def output_diff(self, diff_commands):
        for command in diff_commands.commands:
            left_position, operation, right_position = DiffCommands.extract_command(diff_commands, command)
            print(command, end='')

            if operation[0] == 'a':
                self._output_add(right_position)

            if operation[0] == 'd':
                self._output_delete(left_position)

            if operation[0] == 'c':
                self._output_delete(left_position)
                print('---')
                self._output_add(right_position)

    def output_unmodified_from_original(self, diff_commands):
        file_1_copy = deepcopy(self.file_1_content)
        unmodified_original_file = self._output_unmodified_file(diff_commands, file_1_copy, 1)
        for line in unmodified_original_file:
            print(line, end='')

    def output_unmodified_from_new(self, diff_commands):
        file_2_copy = deepcopy(self.file_2_content)
        unmodified_new_file = self._output_unmodified_file(diff_commands, file_2_copy, 2)
        for line in unmodified_new_file:
            print(line, end='')

    def get_all_diff_commands(self):
        file1 = deepcopy(self.file_1_content)
        file2 = deepcopy(self.file_2_content)
        lcs_dict = {}
        self.get_lcs(file1, file2, lcs_dict)
        lcs = lcs_dict[f'file1[:{len(file1)}]&file2[:{len(file2)}]']

        all_index_file1 = [self.find_all_index(self.file_1_content, x) for x in lcs]
        all_index_file2 = [self.find_all_index(self.file_2_content, x) for x in lcs]

        file1_lcs_index = self.get_possible_lcs_index(all_index_file1)
        file2_lcs_index = self.get_possible_lcs_index(all_index_file2)

        possible_diff = []
        for lcs_file1 in file1_lcs_index:
            for lcs_file2 in file2_lcs_index:
                possible_diff.append(self.get_one_possible_diff(lcs_file1, lcs_file2,
                                                                self.file_1_content, self.file_2_content))
        # Sort the command
        sorted_output = ['\n'.join(one_command) for one_command in sorted(possible_diff)]
        return sorted_output
