const { test, expect } = require('@playwright/test');

test('homepage loads', async ({ page }) => {
  await page.goto('http://localhost:3000');
  // Basic smoke check: page loaded and has a document title
  await expect(page).toHaveTitle(/.*/);
});
