---
layout: single
author: Coen Valk
title: Learning Golang with Advent of Code
excerpt: My initial review of Go based on solving Advent of Code questions.
category: programming
---

[Advent of Code](https://adventofcode.com/) is over, and Santa has successfully
delivered all the presents. As explained in my previous post, I took the Advent
of Code challenge to learn [Golang](https://go.dev/). Here are my initial
thoughts from how I saved Christmas with my newfound Go programming skills.

## What I liked

### Tooling

For my personal projects I use a
[ChromeOS tablet](https://www.lenovo.com/us/en/p/laptops/lenovo/lenovo-edu-chromebooks/lenovo-chromebook-duet-gen-9-11-inch-mediatek/83hh0001us)
with a crostini terminal emulator. It's a nice machine for light coding on the
go, but VSCode makes it a little sluggish. So I use [Neovim](https://neovim.io/)
(BTW). With my neovim config derived from
[Kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim), I found adding
Golang support incredibly easy. All I needed to do was add the gopls (pronounced
["Go, Please"](https://go.dev/gopls/)) language server to Mason and I was ready
to go with syntax highlighting, code completions, and compiler warnings. For
formatting I added the gofmt formatter in Conform. The final thing I changed was
reducing the tab width from 4 to 2; just a personal preference. I was ready to
start my first day of Advent of Code within 10 minutes.

### Syntax

I also quite liked the simple syntax. After programming in Rust for a while the
postfix type annotations felt familiar. For someone mostly familiar with Java or
C this might take some getting used to, as it did for me while first learning
Rust. Either way it didn't matter much, because of how frequently I was able to
use the `:=` type inference syntax sugar. The syntax made it easy to just focus
on hacking together a solution around my busy daily schedule without focusing on
memory management or additional boilerplate code.

I found the error handling easy to understand and enjoyed how it didn't get in
my way. Because the questions always had the same input and I had limited time
in the day to solve the problems, I ended up mostly ignoring the `err` values
returned. Most importantly, I had to actively **choose** to ignore the err
values because each error is returned together with the original value. In more
robust code I could definitely see how easy it would be to handle any errors
that may arise and return early with an error value of our own.

## What I didn't like

### Data manipulation

It could be due to my limited knowledge of the standard library, but I felt like
the data manipulation methods were fairly limited. I found it a bit clunky to
insert and remove elements from slices and containers, and iterating over
elements in a container felt a little inconsistent. Should I use `range`,
`while`, or `for i := container.Front(); i != nil; i = i.Next()`?

Go uses unicode [runes](https://go.dev/blog/strings) to iterate over strings. As
much of the Advent of Code questions rely on alphanumeric charaters, it was a
chore to convert from and to C style bytes. I do like the pattern of
unicode-friendly strings by default, but I would like a C-style string struct
available for these specific types of questions. In retrospect, I should have
used the cgo package to convert to
[C-style](https://go.dev/wiki/cgo#go-strings-and-c-strings) strings once rather
than continuously converting `rune` to `char`.

### Limited data structures

For a few days' solutions I wanted to use a hash set. I was surprised to see
there's no built-in set data structure offered in the standard library. I know,
I know, if you have a map you can treat it like a set by using an empty value
type. In fact, that is exactly what the Rust implementation of
[`HashSet`](https://doc.rust-lang.org/stable/std/collections/struct.HashSet.html)
does. But it seems like it would have been very little effort on the Golang
developers to handle that case in the standard library.

### `any` Type

Unfortunately I can't get dev points by just quipping
["lol no generics"](https://divan.dev/posts/go_complain_howto/) anymore, as
Golang introduced generics with v1.18 in 2022. However, to my disappointment Go
uses an `any` type for some of its generic implementations similar to Python and
Typescript. That means you can write something like this:

```go
l := list.New()

l.PushBack(1)
l.PushBack("hi")
l.PushBack(100)

i := l.Front() // I don't know what type i.Value is!
```

This broke my intuition on Golang's type safety and inference. Even though the
`int[]` slice type would be be the more idiomatic way to refer to a list of
integers, a container implemented in the standard library should have
consistantly typed elements rather than rely on an `any` type. This seems like a
peculiar decision considering `map` and slice require types as part of their
definition and initialization.

## Thoughts

I regret not being able to use the key feature of Golang:
[Goroutines](https://youtu.be/f6kdp27TYZs?si=zFEbHzDf141JLxU3). The problems in
the Advent of Code just aren't right for concurrent programming. My solutions
are just short scripts that take in some text input, perform some simple
calculation, and output a solution for parts 1 and 2. I've heard really good
things about Go's concurrency model and I would like to try it out in a
different project. Perhaps a simple client / server project.

I recognize I should probably list all of my "what I didn't like" points under
"skill issue". I would like to continue learning about all of Go's features
before calling anything a deal-breaker. I've barely scratched the surface of
what Go is capable of. I'm looking forward to learning more about it and using
it in future projects!
