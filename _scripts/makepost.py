#! /usr/bin/env python3

import argparse
import datetime
import pathlib
import re


POST_TEMPLATE = '''---
layout: post
category: {category}
title: {title}
---'''

CATEGORY_TEMPLATE = '''---
layout: category
title: {title}
permalink: /{title}
---'''


def main():
    p = argparse.ArgumentParser('Create a post')
    p.add_argument('title')
    p.add_argument('category')
    args = p.parse_args()

    path = pathlib.Path(__file__).absolute().parents[1]
    category = path.joinpath(f'{args.category}.md')
    if not category.exists():
        print(f'creating category: {args.category}')
        with category.open('w') as file:
            file.write(CATEGORY_TEMPLATE.format(title=args.category))

    filename = re.sub('[^\w\-_\.]', '_', args.title)
    filename = re.sub('_{2,}', '_', filename)
    d = datetime.date.today().isoformat()
    post = path.joinpath(f'_posts/{d}-{filename}.md')
    with post.open('w') as file:
        file.write(POST_TEMPLATE.format(title=args.title, category=args.category))

if __name__ == "__main__":
    main()