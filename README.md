# auditree.github.io
This homepage is rendered by [Jekyll][] and hosted on [Github pages][].

## New posts

Posts are markdown files, and are stored in `_posts`. You should create a new post, which auto generates the necessary YAML header, by running:

```
_scripts/makepost.py 'Your post title' your-post-category
```

If the category is new, a stub file will be created for it in the top level directory. These stubs are used to build a category index. You will need to commit this file as well as the post file to git.

You can run `jekyll serve` in the top directory of the site to serve a local copy of the site & verify markdown or any edits to styling, layouts or includes at http://localhost:4000. The built artefacts will be in `_site`, which can be useful for debugging.

## Editing the layout & appearance

Pages are given a layout (in `_layouts`) which may use one or more include (from `_includes`). The site's CSS is in `style.css`

[Jekyll]: https://jekyllrb.com/
[Github pages]: https://pages.github.com/