---
layout: single
author: Coen Valk
title: How to Become a Mastermind
excerpt: Revisiting code I wrote in highschool. Can I do better today?
category: school
tags:
  - C
---

In 11th and 12th grade I was enrolled in the
[International Baccalaureate](https://www.ibo.org/about-the-ib/) program at my
[high-school](https://www.nordangliaeducation.com/village-houston). Part of my
higher-level math class curriculum was writing a 2,000 word essay on a math
topic of my choosing. I enjoyed programming and I wanted to find a way to
incorporate it into my project. I had recently learned about famous computer
scientist and author of
[_The Art of Computer Programming_](https://cs.stanford.edu/~knuth/taocp.html)
Donald Knuth. One of
[Donald Knuth's](https://en.wikipedia.org/wiki/Donald_Knuth) earlier papers -
[_The Computer as a Mastermind_](https://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf)
caught my eye, and I decided I could replicate its results. I learned about the
board game
[Mastermind](https://en.wikipedia.org/wiki/Mastermind_%28board_game%29), read up
on [minimax](https://en.wikipedia.org/wiki/Minimax) decision making, and wrote
some [C code](https://github.com/coenvalk/mastermind) that followed Knuth's
winning strategy. I submitted my paper
[_How to Become a Mastermind_](https://drive.google.com/file/d/0B8CNl_hZHtFzTm5ESzZ0QVRLV0k/view?resourcekey=0-n8PlszyU4NrlLWrGLp0REA)
proud of the work I did and the things I learned.

_As an aside: this was also the first paper I ever wrote in
[$$ \LaTeX $$](https://www.latex-project.org/) after learning about the
typesetting program at a math and programming pre-college summer camp I
attended. I was very pleased with myself._

After a few weeks of waiting I received back a mark of 6 out of 7 - a very
respectable score. At the time I was a little disappointed I didn't get full
marks considering all the hard work I put in, but I eventually made peace with
my grade.

That was 8 years ago. Since then, I have learned a lot more about programming,
math, and science communication. As an exercise in reflection and growth, I want
to share some thoughts on my code, my writing, and how I would approach the
problem differently today.

## The Good

Honestly - for a high-school project? Good effort. The code _works_ and has no
memory leaks which is already more than I can say for some of my other projects.
I even included a
[Makefile](https://github.com/coenvalk/mastermind/blob/master/Makefile) and
[MIT license](https://github.com/coenvalk/mastermind/blob/master/LICENSE)! The
underlying math in the paper is correct, with a few small nit-picky inaccuracies
which we will discuss later. The writing is mostly understandable, with perhaps
a slight over reliance on complicated math jargon and notation to make the topic
sound more advanced than it actually is. The paper is well cited and all
citations are properly formatted (thanks $$\LaTeX$$!) Finally, most impressive
perhaps is the fact that we didn't have Chat GPT in those days to write essays
for us.

## The Bad

Nevertheless, I come to bury me, not to praise me. There is a lot we can improve
here.

### The Math

The math is a little jumbled. The explanations are wordy (hey - I had to hit
that 2,000 word count somehow, right?) and the notation can be simplified. Just
look at the difference between Knuth's overall explanation of minimax algorithm
and mine:

> Figure 1 was found by choosing at every stage a test pattern that _minimizes
> the maximum number of remaining possibilities_ over all of the 15 responses by
> the codemaker.
>
> &mdash; Donald Knuth, 1976

In one sentence, Knuth accurately summarizes the algorithm used to find the next
test pattern.

> The best guess given a set S where the secret code is still an element is the
> code that the worst case response, the response that decreases S the least, is
> minimized.
>
> &mdash; Coen Valk, 2016

While it still boils down to a single sentence summary, mine is much more
difficult to understand. It has unnecessary and confusing set theory jargon and
the commas are in the wrong place. While I still have a nasty habit of being a
bit too verbose, I've learned that understanding after a first reading is much
more important than cramming a bunch of math on a page.

### Memory Allocations

After running the compiled program with Valgrind I was pleased to see that high
school Coen had remembered to take care of all memory leaks! However, something
else stood out to me in the heap summary:

```bash
...
Yay! I win!
==16554==
==16554== HEAP SUMMARY:
==16554==     in use at exit: 0 bytes in 0 blocks
==16554==   total heap usage: 874,095 allocs, 874,095 frees, 3,499,712 bytes allocated
==16554==
==16554== All heap blocks were freed -- no leaks are possible
==16554==
==16554== For lists of detected and suppressed errors, rerun with: -s
==16554== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

Nearly 900K heap allocations for a simple program like this seems pretty high.
By far the largest number of heap allocations come from how I create codes on
the fly rather than keep a full list of every possible code in memory at the
same time. This is a useful pattern for when we want to play the game with a
longer code or more possible colors, as the set of possible solutions grows
exponentially in size. That does mean the `get_code()` function is called
frequently in loops like this:

```c
unsigned char *get_code(int length, unsigned char colors, int index)
{
  unsigned char *code = (unsigned char *)malloc(length * sizeof(unsigned char));
  int i;
  for (i = 0; i < length; i++)
  {
    code[length - i - 1] = index % colors;
    index /= colors;
  }
  return code;
}

void print_all_guesses(bool *S, int n, int length, unsigned char colors)
{ // Prints all current possibilities
  int i;
  for (i = 0; i < n; i++)
  {
    if (S[i])
    {
      unsigned char *C = get_code(length, colors, i);
      print_guess(C, length);
      free(C);
      printf(", ");
    }
  }
  printf("\n");
}
```

In each loop iteration, I create and almost immediately free the `code` object.
Instead, I could allocate space once and re-use the same object:

```c
void get_code_inplace(
  int length, unsigned char colors, int index, unsigned char *code)
{
  int i;
  for (i = 0; i < length; i++)
  {
    code[length - i - 1] = index % colors;
    index /= colors;
  }
}

void print_all_guesses(bool *S, int n, int length, unsigned char colors)
{ // Prints all current possibilities
  int i;
  unsigned char *code = calloc(sizeof(unsigned char), length);
  for (i = 0; i < n; i++)
  {
    if (S[i])
    {
      get_code_inplace(length, colors, i, code);
      print_guess(code, length);
      printf(", ");
    }
  }
  printf("\n");
  free(code);
}
```

Now let's look at the number of memory allocations:

```bash
...
Yay! I win!
==18231==
==18231== HEAP SUMMARY:
==18231==     in use at exit: 0 bytes in 0 blocks
==18231==   total heap usage: 3,851 allocs, 3,851 frees, 18,736 bytes allocated
==18231==
==18231== All heap blocks were freed -- no leaks are possible
==18231==
==18231== For lists of detected and suppressed errors, rerun with: -s
==18231== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

With a few small tweaks, we can reduce the number of memory allocations by two
orders of magnitude.

### Performance

Choosing the first move is a relatively large search space. My program brute
force checks for each possible guess and feedback, the number of possible
guesses would still be left. This ends up being $$ O\left( c^{2l} \cdot l^2
\right) $$ where c is the number of colors and l is the length of the code.
There's a lot of duplicated work happening in `full_reduce()`, in which I
compare the number of possible solutions that could match the feedback given:

```c
int reduce(
  bool* S,
  unsigned char* now,
  int c,
  int p,
  int length,
  unsigned char colors,
  int n
) {
  int x = 0;
  int i;
  for (i = 0; i < n; i++) {
    if (S[i]) {
      unsigned char* Code = get_code(length, colors, i);
      int r* = analyze(Code, now, length, colors);
      free(Code);
      if (r[0] == c && r[1] == p) x++;
      free(r);
    }
  }
  return x;
}

int fullReduce(
  bool* S, unsigned char* now, int length, unsigned char colors, int n) {
  int responses[13][2] = { 
    {0, 0},
    {1, 0},
    {0, 1},
    {2, 0},
    {1, 1},
    {0, 2},
    {3, 0},
    {2, 1},
    {1, 2},
    {0, 3},
    {4, 0},
    {3, 1},
    {2, 2}};
  int x = 0;
  int index = 0;
  int i;
  for (i = 0; i < 13; i++) { // loop through all possible feedback values
    // return number of codes would give back this exact feedback response:
    int y = reduce(S, now, responses[i][0], responses[i][1], length, colors, n);
    if (y > x) {
      x = y;
      index = i;
    }
  }
  return x;
}
```

With this strategy I compare each code with every other code 13 times - one for
each possible feedback response. I can instead compare all possible guesses and
solutions with each other once and count up the amount of times a certain
feedback is observed:

```c
int max_feedback_result(
  bool *solution_set, unsigned char *guess, int length, unsigned char colors)
{
  struct Feedback feedback;
  size_t *feedback_buckets = calloc(sizeof(size_t), length * length + 1);
  size_t largest_feedback_bucket_size = 0;
  size_t n = pow(colors, length);
  unsigned char *possible_solution = calloc(sizeof(unsigned char), length);

  for (size_t i = 0; i < n; ++i)
  {
    if (!solution_set[i])
      continue;

    get_code_inplace(length, colors, i, possible_solution);
    get_feedback(possible_solution, guess, length, colors, &feedback);
    feedback_buckets[feedback.pegs_in_correct_place * length + feedback.pegs_with_correct_color]++;
  }

  for (size_t i = 0; i < length * length; ++i)
  {
    if (feedback_buckets[i] > largest_feedback_bucket_size)
    {
      largest_feedback_bucket_size = feedback_buckets[i];
    }
  }

  free(feedback_buckets);
  free(possible_solution);

  return largest_feedback_bucket_size;
}
```

_This also makes the program extendable to longer lengths for free, because the
feedback responses are no longer hard coded into the program! I remember racking
my brain to try and find an algorithm to find the number of possible feedback
values for any given length, and giving up after the code took too long to run
at longer code lengths anyway._

this brings the run time down considerably:

```bash
finding best move took 274 milliseconds
```

There are likely further optimizations I can make, but for the purposes of this
exercise I'm pleased with this speed up.

## The Ugly

The most glaring ugliness is the function and variable naming. There is no case
consistency at all. `snake_case`, `camelCase`, and `PascalCase` are all used
interchangeably. Variables are frequently single letters, without a clear way to
infer what they mean. Thankfully in modern IDEs this, as well as re-formatting
the entire document, can be done automatically with little effort at all.

Let's take the `analyze()` function as an example of difficult to read code:

```c
int *analyze(
  unsigned char *code, unsigned char *guess, int length, unsigned char colors)
{
  int i;
  int c = 0;
  int p = 0;
  for (i = 0; i < colors; i++)
  {
    int gue = howmany(i, guess, length);
    int cod = howmany(i, code, length);
    if (cod > gue)
      c += gue;
    else
      c += cod;
  }
  for (i = 0; i < length; i++)
  {
    if (isin(guess[i], code, length))
    {
      if (guess[i] == code[i])
      {
        p++;
      }
    }
  }
  int *r = (int *)malloc(sizeof(int) * 2);
  r[0] = c - p;
  r[1] = p;
  return r;
}
```

Function and variable names are not descriptive, making the logic difficult to
follow. While I'm not a "self-documenting" code expert, there's a lot we can
change to make this more readable, as well as reduce more memory allocations by
incorporating the same pattern as above:

```c
struct feedback {
  int pegs_in_correct_place;
  int pegs_with_correct_color;
}

...

void get_feedback(
  unsigned char *potential_solution, 
  unsigned char *guess, 
  int length, 
  unsigned char colors, 
  struct Feedback *out_feedback)
{
  int pegs_in_correct_place = 0;
  int pegs_with_correct_color = 0;
  for (int color = 0; color < colors; color++)
  {
    int color_pegs_in_guess = count_all_instances(color, guess, length);
    int color_pegs_in_solution = count_all_instances(color, potential_solution, length);

    if (color_pegs_in_solution > color_pegs_in_guess)
      pegs_with_correct_color += color_pegs_in_guess;
    else
      pegs_with_correct_color += color_pegs_in_solution;
  }

  for (int idx = 0; idx < length; idx++)
  {
    if (guess[idx] == potential_solution[idx])
    {
      pegs_in_correct_place++;
    }
  }

  // subtract pegs in correct place from pegs with matching color to remove duplicates
  pegs_with_correct_color -= pegs_in_correct_place;

  out_feedback->pegs_in_correct_place = pegs_in_correct_place;
  out_feedback->pegs_with_correct_color = pegs_with_correct_color;
}
```

### Repeated work

There are several areas in the code where I perform the same action multiple
times. in the `main()` function I reduce the set of possible solutions twice in
a row:

```c
newN = reduce(S, move, c, p, length, colors, n);
SetReduce(S, move, c, p, length, colors, n);
```

Now I only perform the `reduce()` operation once per turn while I still get all
the information I need by returning the number of remaining candidates directly
from `set_reduce()`

```c
remaining_candidates = set_reduce(
  solution_set,
  move,
  pegs_with_correct_color,
  pegs_in_correct_place,
  length,
  colors
);
```

This makes the code easier to parse and reduces unnecessary extra work.

## Finally

[The full diff is available on GitHub](https://github.com/coenvalk/mastermind/pull/1/files).
After all is said and done, I greatly reduced the number of memory allocations,
improved runtime performance, and made the code easier to read and understand
with code comments and better naming. Looks like in the past 8 years I [learned
a thing or two]({% link _pages/resume.md %}) after all!
