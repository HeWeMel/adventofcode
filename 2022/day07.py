from collections import defaultdict
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        local_size = defaultdict(int)
        local_dirs = defaultdict(set)
        local_files = defaultdict(set)
        path = []
        for line in text.splitlines():
            path_tuple = tuple(path)
            match line.split():
                case ["$", "cd", "/"]:
                    path = ["/"]
                case ["$", "cd", ".."]:
                    path.pop()
                case ["$", "cd", cd_dir]:
                    path.append(cd_dir)
                case ["$", "ls"]:
                    continue
                case ["$", *others]:
                    raise RuntimeError("illegal command {}".format(line))
                case ["dir", dir_name]:
                    local_dirs[path_tuple].add(dir_name)
                case [size_txt, file_name]:
                    if file_name not in local_files[path_tuple]:  # path might be ls'ed twice
                        local_files[path_tuple].add(file_name)
                        local_size[path_tuple] += int(size_txt)

        paths = set().union(local_size.keys(), local_dirs.keys(), local_files.keys())
        d.global_size = dict()
        for path in reversed(sorted(list(paths))):  # subdirectories before their parents
            d.global_size[path] = local_size[path] + sum(d.global_size[path + (local_dir,)]
                                                         for local_dir in local_dirs[path])

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return sum(d.global_size[path]
                   for path in d.global_size.keys()
                   if d.global_size[path] <= 100000)

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve('''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''), 95437, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        to_be_freed = 30000000 - (70000000 - d.global_size[("/",)])
        sorted_sizes = sorted([d.global_size[path]
                               for path in d.global_size.keys()
                               if d.global_size[path] >= to_be_freed
                               ])
        return sorted_sizes[0]

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve('''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''), 24933642, "example"

Day.do_day(day=7, year=2022, part_a=PartA, part_b=PartB)
