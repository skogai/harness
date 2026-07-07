import { readFile, writeFile } from 'fs/promises';
import { pathExists, ensureDir } from 'fs-extra';
import { dirname } from 'path';

function markers(tag, commentPrefix) {
  const prefix = commentPrefix ? `${commentPrefix} ` : '';
  return {
    begin: `${prefix}<${tag}>`,
    end: `${prefix}</${tag}>`,
  };
}

/**
 * Insert or replace a tagged managed block in a file, preserving all
 * content outside the markers. Creates the file if it does not exist.
 * `commentPrefix` (e.g. "#") wraps the tag in a line comment for formats
 * where a bare `<tag>` isn't valid syntax, such as TOML.
 */
export async function upsertManagedBlock(filePath, tag, content, { commentPrefix } = {}) {
  const { begin, end } = markers(tag, commentPrefix);
  const block = `${begin}\n${content.trim()}\n${end}`;

  if (!(await pathExists(filePath))) {
    await ensureDir(dirname(filePath));
    await writeFile(filePath, `${block}\n`, 'utf-8');
    return filePath;
  }

  const existing = await readFile(filePath, 'utf-8');
  const beginIndex = existing.indexOf(begin);
  const endIndex = existing.indexOf(end);

  let next;
  if (beginIndex !== -1 && endIndex !== -1 && endIndex > beginIndex) {
    next = existing.slice(0, beginIndex) + block + existing.slice(endIndex + end.length);
  } else if (beginIndex === -1 && endIndex === -1) {
    const separator = existing.endsWith('\n') ? '\n' : '\n\n';
    next = `${existing}${separator}${block}\n`;
  } else {
    throw new Error(`Corrupted <${tag}> markers in ${filePath}. Remove the stray marker and re-run sync.`);
  }

  await writeFile(filePath, next, 'utf-8');
  return filePath;
}

export async function readManagedBlock(filePath, tag, { commentPrefix } = {}) {
  const { begin, end } = markers(tag, commentPrefix);
  if (!(await pathExists(filePath))) {
    return null;
  }
  const existing = await readFile(filePath, 'utf-8');
  const beginIndex = existing.indexOf(begin);
  const endIndex = existing.indexOf(end);
  if (beginIndex === -1 || endIndex === -1 || endIndex < beginIndex) {
    return null;
  }
  return existing.slice(beginIndex + begin.length, endIndex).trim();
}
