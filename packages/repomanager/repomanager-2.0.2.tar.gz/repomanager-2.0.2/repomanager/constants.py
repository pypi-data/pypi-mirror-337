
import os

root = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()
r_clone = 'git clone --progress --filter=blob:none {0}-b {1} {2} {3} {4};'
r_fetch = 'git fetch {0}origin {1}'
r_reset = 'git reset --hard'
r_checkout = 'git -c advice.detachedHead=false checkout {0} --recurse-submodules'
r_currcommit = 'git rev-parse HEAD'
r_branchcommit = 'git rev-parse {0}'
r_diff = 'git diff'
r_checkpatch = 'git apply --check {0}'
r_applypatch = 'git apply {0}'
r_checkunpatch = 'git apply -R --check {0}'
r_applyunpatch = 'git apply -R {0}'
r_sparseconfig = 'git init ;\
        git config core.sparseCheckout true ;\
        git remote add origin {0} ;\
        git sparse-checkout set --cone ;\
        echo "{1}" > .git/info/sparse-checkout ;\
        git fetch {2}--filter=blob:none origin {3} ;\
        git checkout FETCH_HEAD'
r_real_sparseconfig = 'git init ;\
        git config core.sparseCheckout true ;\
        git remote add origin {0} ;\
        echo "{1}" > .git/info/sparse-checkout ;\
        git fetch --depth 1 origin {2} ; \
        git checkout FETCH_HEAD'
