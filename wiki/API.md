# Auditeo AI API Documentation

This document outlines the available endpoints for the Auditeo AI API.

## Base URL

By default, the API runs on `http://localhost:8000`.

---

## 1. Run Website Audit

Executes a full audit flow on a given website URL. This process extracts factual metrics, generates KPI scores, creates an insights report, and provides actionable recommendations.

**Endpoint:** `/api/audit`  
**Method:** `POST`  
**Content-Type:** `application/json`

### Request Body

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `website_url` | `string` | Yes | The full URL of the website to audit (e.g., `https://example.com`). |

**Example Request Payload:**
```json
{
  "website_url": "https://example.com"
}
```

### Example cURL Request

```bash
curl -X POST http://localhost:8000/api/audit \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: custom-trace-id-123" \
  -d '{
    "website_url": "https://example.com"
  }'
```
*(Note: `X-Request-ID` header is optional but recommended for tracing requests.)*

### Response

The response is wrapped in a standard `APIResponse` object containing `success`, `trace_id`, `message`, and `data`.

**Status Codes:**
- `200 OK`: Audit completed successfully.
- `500 Internal Server Error`: Audit flow failed.

**Example Successful Response (200 OK):**

```json
{
  "success": true,
  "trace_id": "custom-trace-id-123",
  "message": "Audit flow executed successfully",
  "data": {
    "website_url": "https://example.com",
    "factual_metrics": {
      "total_word_count": 1250,
      "heading_counts": {
        "h1": 1,
        "h2": 6,
        "h3": 12
      },
      "cta_count": 4,
      "link_counts": {
        "internal": 25,
        "external": 8
      },
      "image_count": 10,
      "images_missing_alt_text_pct": 20.0,
      "meta_title": "Example Domain - Home",
      "meta_description": "This domain is for use in illustrative examples in documents."
    },
    "kpis": {
      "seo_score": 85,
      "links_score": 78,
      "usability_score": 92,
      "social_score": 65
    },
    "insights_report": "# Website Audit Report\n\n## Overview\nThe website demonstrates strong usability but lacks in some SEO areas...\n\n*(Full Markdown report content)*",
    "recommendations": [
      {
        "priority": 1,
        "title": "Add Alt Text to Images",
        "action": "Update the <img> tags for the 2 images missing alt attributes to include descriptive text.",
        "reasoning": "20% of images are missing alt text, which negatively impacts accessibility and image search SEO.",
        "expected_impact": "Improved accessibility compliance and potential increase in organic traffic from image searches."
      },
      {
        "priority": 2,
        "title": "Increase External Links",
        "action": "Add 2-3 authoritative external links to support claims in the main content.",
        "reasoning": "The current external link count is relatively low for a page of 1250 words.",
        "expected_impact": "Enhanced page authority and trustworthiness signals for search engines."
      }
    ]
  }
}
```

### Response Data Schema Details

#### `data.factual_metrics`
- `total_word_count` (int): Total number of words in the page content.
- `heading_counts` (object): Counts for heading tags (`h1`, `h2`, `h3`).
- `cta_count` (int): Number of calls-to-action (buttons or primary action links).
- `link_counts` (object): Counts for links (`internal`, `external`).
- `image_count` (int): Total number of images.
- `images_missing_alt_text_pct` (float): Percentage of images missing alt text (0.0 to 100.0).
- `meta_title` (string | null): Content of the `<title>` tag.
- `meta_description` (string | null): Content of the meta description tag.

#### `data.kpis`
- `seo_score` (int): The SEO score of the page (0-100).
- `links_score` (int): The links score of the page (0-100).
- `usability_score` (int): The usability score of the page (0-100).
- `social_score` (int): The social score of the page (0-100).

#### `data.recommendations` (Array of Objects)
- `priority` (int): Priority level (1 being highest, up to 5).
- `title` (string): Concise, actionable title of the recommendation.
- `action` (string): Step-by-step instructions on what to implement.
- `reasoning` (string): Logical justification tied strictly to the extracted metrics.
- `expected_impact` (string): The predicted outcome for SEO or Conversion.
