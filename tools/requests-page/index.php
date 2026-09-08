<?php
// The human validator: the review page for the Arctic history researchers'
// request queue, served at cryomics.org/amundsen/requests/ behind basic auth.
//
// Grid pushes the queue here as requests.json and collects the decisions from
// answers.json with tools/requests-sync.py; this page only reads the one and
// writes the other. Everything shown is researcher-written text: escape it.

$dir = __DIR__;
$feed = json_decode(@file_get_contents("$dir/requests.json") ?: '{}', true) ?: [];
$requests = $feed['requests'] ?? [];
$generated = $feed['generated'] ?? '';
$answers = json_decode(@file_get_contents("$dir/answers.json") ?: '{}', true) ?: [];
$msg = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = (string) (int) ($_POST['id'] ?? 0);
    $status = $_POST['status'] ?? '';
    $answer = trim($_POST['answer'] ?? '');
    $known = false;
    foreach ($requests as $r) {
        if ((string) $r['id'] === $id && $r['status'] === 'open') { $known = true; }
    }
    if ($known && in_array($status, ['approved', 'denied', 'done'], true)) {
        $answers[$id] = ['status' => $status, 'answer' => $answer, 'at' => gmdate('c')];
        file_put_contents("$dir/answers.json",
            json_encode($answers, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), LOCK_EX);
        header('Location: ' . strtok($_SERVER['REQUEST_URI'], '?'));
        exit;
    }
    $msg = 'not saved: unknown request or bad status';
}

function h($s) { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
$open = array_filter($requests, fn($r) => $r['status'] === 'open' && !isset($GLOBALS['answers'][(string) $r['id']]));
$pending = array_filter($requests, fn($r) => $r['status'] === 'open' && isset($GLOBALS['answers'][(string) $r['id']]));
$closed = array_filter($requests, fn($r) => $r['status'] !== 'open');
?>
<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Amundsen history: requests</title>
<style>
  body { font: 15px/1.5 system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; color: #222; }
  h1 { font-size: 1.3rem; } h2 { font-size: 1.05rem; margin-top: 2rem; }
  .req { border: 1px solid #ccc; border-radius: 6px; padding: .8rem 1rem; margin: .8rem 0; }
  .req.closed, .req.pending { color: #666; background: #f7f7f7; }
  .meta { font-size: .85rem; color: #666; }
  .what { font-weight: 600; }
  textarea { width: 100%; box-sizing: border-box; min-height: 3.5rem; font: inherit; margin: .4rem 0; }
  .note { color: #666; font-size: .9rem; }
  .warn { color: #a00; }
  form { margin: .5rem 0 0; }
</style>
<h1>Arctic history research: requests</h1>
<p class="note">Queue as of <?= h($generated ?: 'never pushed') ?>.
Decisions saved here are collected by grid every few minutes; researchers read
them with <code>history-db.py requests</code>.</p>
<?php if ($msg): ?><p class="warn"><?= h($msg) ?></p><?php endif; ?>

<h2>Waiting for you (<?= count($open) ?>)</h2>
<?php if (!$open): ?><p class="note">Nothing waiting.</p><?php endif; ?>
<?php foreach ($open as $r): ?>
  <div class="req">
    <div class="meta">#<?= h($r['id']) ?> · <?= h($r['kind']) ?> · <?= h($r['topic']) ?>
      · <?= h($r['created']) ?><?= $r['who'] ? ' · ' . h($r['who']) : '' ?></div>
    <div class="what"><?= h($r['what']) ?><?= $r['size_mb'] ? ' (' . h(round($r['size_mb'])) . ' MB)' : '' ?></div>
    <?php if ($r['why']): ?><div><?= h($r['why']) ?></div><?php endif; ?>
    <?php if ($r['url'] && preg_match('#^https?://#', $r['url'])): ?>
      <div><a href="<?= h($r['url']) ?>" rel="noreferrer"><?= h($r['url']) ?></a></div>
    <?php elseif ($r['url']): ?><div><?= h($r['url']) ?></div><?php endif; ?>
    <?php if ($r['dest']): ?><div class="meta">should land at <?= h($r['dest']) ?></div><?php endif; ?>
    <form method="post">
      <input type="hidden" name="id" value="<?= h($r['id']) ?>">
      <textarea name="answer" placeholder="your answer to the researcher"></textarea>
      <button name="status" value="approved">approve</button>
      <button name="status" value="denied">deny</button>
      <button name="status" value="done">done</button>
    </form>
  </div>
<?php endforeach; ?>

<?php if ($pending): ?>
<h2>Decided here, not yet collected by grid (<?= count($pending) ?>)</h2>
<?php foreach ($pending as $r): $a = $answers[(string) $r['id']]; ?>
  <div class="req pending">
    <div class="meta">#<?= h($r['id']) ?> · <?= h($r['kind']) ?> · <?= h($r['topic']) ?></div>
    <div class="what"><?= h($r['what']) ?></div>
    <div><?= h($a['status']) ?><?= $a['answer'] !== '' ? ': ' . h($a['answer']) : '' ?></div>
  </div>
<?php endforeach; endif; ?>

<h2>Resolved (<?= count($closed) ?>)</h2>
<?php foreach ($closed as $r): ?>
  <div class="req closed">
    <div class="meta">#<?= h($r['id']) ?> · <?= h($r['kind']) ?> · <?= h($r['topic']) ?>
      · <?= h($r['resolved']) ?></div>
    <div class="what"><?= h($r['what']) ?></div>
    <div><?= h($r['status']) ?><?= $r['answer'] !== '' ? ': ' . h($r['answer']) : '' ?></div>
  </div>
<?php endforeach; ?>
