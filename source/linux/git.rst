Git
====


 - 清空Commit记录

  .. code-block:: bash
     
     #checkout
     git checkout --orphan latest_branchgit add -A
     
     # 提交
     git add -A && git commit -m "commit message"

     #删除分支
     git branch -D master
     #重命名当前分支并强制更新当前存储库
     git branch -m master && git push -f origin master

     #默认对当前commit进行tag, 如需指定，可以指定commit id
     git tag $tagname $commit

     #push 包含tag
     git push --tags
