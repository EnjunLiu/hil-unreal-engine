# Semantic-free entity refactor patches

Cloud agent could not push to `EnjunLiu/asv-vla-training` or `EnjunLiu/asv-jetson-ws` (403 for cursor[bot]).

Apply on those remotes:

```bash
cd asv-vla-training && git am tools/semantic-free-entity-refactor/training/*.patch
# or: git apply tools/semantic-free-entity-refactor/asv-vla-training.patch

cd asv-jetson-ws && git am tools/semantic-free-entity-refactor/jetson/*.patch
```

UE side: no code changes this phase (simulator IDs remain opaque data).
