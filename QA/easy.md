# Website bugs — simple version

Handoff updated **7 October 2026**: **12 open bugs — 2 Client, 10 Developer**. Original bug numbers are unchanged. Evidence dates: 5–6 October 2026. This is the selected work scope, not a new website retest.

Use the live links to check each problem. Do not complete a payment or submit a real enquiry while checking.

## Client will fix

### BUG-006 — Return rules are missing and disagree
The Returns page talks about whether the company is legitimate, but does not explain how to return an item. Other pages promise both **15 days** and **30 days**.

[Check Returns](https://www.houseofdiams.com/returns) · [Check product return details](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · BUG-006

### BUG-013 — Unfinished test text is visible
Shipping shows **“NEW TEST BLACK”** and **“test desc”**. Cart/checkout shows **“This is new pointer”**, and the top announcement also showed **“New line”**.

[Check Shipping](https://www.houseofdiams.com/shipping) · [Check cart](https://www.houseofdiams.com/cart) · BUG-013

## Developer will fix

### BUG-002 — Checkout shows different prices for the same items
With India/rupees selected and items in your cart, compare checkout's item prices with its total. The bracelet showed **₹335** in one place and **₹32,257** in another.

[Check checkout](https://www.houseofdiams.com/checkout?mode=cart) · BUG-002

### BUG-003 — “Forgot your password?” does not help
Click **Forgot your password?** It keeps you on the login page instead of opening password recovery.

[Check login](https://www.houseofdiams.com/login) · BUG-003

### BUG-004 — WhatsApp link has an incomplete phone number
After the page loads, its chat link uses only **91**, instead of the full business number. This stops it from pointing to the intended WhatsApp contact.

[Check homepage chat](https://www.houseofdiams.com/) · BUG-004

### BUG-005 — Keyboard users can land on invisible menu items
On a computer, leave the mobile menu closed and press **Tab** through the header. The selection moves into hidden menu items, making navigation confusing.

[Check homepage](https://www.houseofdiams.com/) · BUG-005

### BUG-008 — Important pages load slowly
In our mobile speed checks, the main content took about **7–18 seconds** to appear. The bracelet page has a very large video and was especially slow.

[Check bracelet](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [Check homepage](https://www.houseofdiams.com/) · BUG-008

### BUG-009 — Cart does not show the bracelet length you selected
Choose **7 Inch** or **7.5 Inch**, then add the bracelet to your bag. The cart leaves out that length and shows an unrelated ring size, **US 4**. Checkout also leaves out the length.

[Choose bracelet length](https://www.houseofdiams.com/shop/rosette-five-flower-bracelet) · [Check cart](https://www.houseofdiams.com/cart) · BUG-009

### BUG-010 — Coupon quiz accepts an incorrect email
Open **Get Your Coupon Code**, enter a name, then enter **invalid** as the email. **Next** still moves forward. Stop before the final submission.

[Check coupon quiz](https://www.houseofdiams.com/) · BUG-010

### BUG-012 — Email link opens a different address
The page displays **Admin@houseofdiams.com**, but clicking it opens an email to **info@houseofdiams.com**. The displayed address and recipient should agree.

[Check Contact](https://www.houseofdiams.com/contact) · BUG-012

### BUG-015 — Two category pictures do not load
On the HipHop Chains page, two category pictures are broken and appear empty.

[Check HipHop Chains](https://www.houseofdiams.com/hiphop/chains) · BUG-015

### BUG-020 — Search suggests a product that does not exist
Open Search without typing and choose **Fine Jewellery Test Product**. It leads to a **page not found** message.

[Open homepage Search](https://www.houseofdiams.com/) · [Check missing product](https://www.houseofdiams.com/shop/fine-jewellery-test-product) · BUG-020

For full steps and all recorded results, open [the main detailed report](main.md#bugs).
