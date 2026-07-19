# Feature Decomposition Rules

## Levels

- **Planning block:** a source heading, paragraph, table row, or media note.
- **Level-one feature:** a recognizable product area kept in source order.
- **Child feature:** a coherent subsystem or behavior group.
- **Atomic function:** the smallest unit that can be independently planned, implemented, tested, and accepted.

## Stop Splitting Only When

An atomic function has one primary objective, a clear trigger, observable outcome, bounded ownership, and standalone acceptance criteria. It should not mix unrelated data, UI, animation, persistence, platform, and flow changes.

## Split Triggers

Split when source text includes independent clauses or lifecycle transitions such as:

```text
并且、同时、之后、播完后、如果、若、否则、首次、每次、重开、复活、首页也要、配置表增加、文本需要多语言
```

Also split when one requirement contains multiple:

- screens or systems;
- trigger conditions;
- states or transitions;
- data/config changes;
- persistence boundaries;
- resource disciplines;
- independently testable outcomes.

## Required Separations

Prefer separate atomic functions for:

1. data schema and defaults;
2. runtime data loading and compatibility;
3. UI entry and visibility;
4. popup content and navigation;
5. input or operation locking;
6. animation trigger and completion;
7. localization registration;
8. persistence and daily/session reset;
9. analytics/advertising/platform mapping;
10. audio, vibration, and art delivery;
11. error handling and conflict resolution.

Do not over-split a single local text/style change into artificial tasks.

## Dependency Rules

Record dependencies as IDs and classify them:

- `blocks`: this function must finish first;
- `requires`: implementation relies on another function;
- `coordinates-with`: parallel disciplines must align;
- `conflicts-with`: simultaneous behavior requires explicit resolution.

## Source Fidelity

For every atomic function, preserve:

- source heading path;
- source requirement summary;
- numerical values or placeholders;
- conditions and exceptions;
- media references;
- whether the item is explicit, inferred, or unresolved.

Do not turn an example into a mandatory implementation unless the source explicitly requires it.

## Example

Planning statement:

```text
道具解锁动画播放期间屏蔽所有操作、弹窗、动画，播完后再出现道具用法操作引导。
```

Candidate atomic functions:

1. determine prop-unlock trigger;
2. start unlock animation;
3. acquire global operation lock;
4. block or queue popup requests;
5. define handling for competing animations;
6. handle unlock-animation completion;
7. release locks safely;
8. start prop usage guide;
9. ensure repeat-entry idempotency and cleanup.
