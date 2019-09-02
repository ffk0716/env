cmake_minimum_required(VERSION 3.15)
project(man NONE)

add_custom_command(OUTPUT man1
    COMMAND mkdir -p man1)
add_custom_target(gen_dir
    DEPENDS man1)

add_custom_command(OUTPUT man1/git-mr.1
    COMMAND pandoc -s -t man git-mr.md > man1/git-mr.1
    DEPENDS gen_dir git-mr.md)
add_custom_target(gen_git_mr ALL
    DEPENDS man1/git-mr.1)
