export default {
  async fetch(request, env, ctx) {
    const response = await fetch(request);
    const url = new URL(request.url);

    // If the request is for a PDF file, inject canonical HTTP headers
    if (url.pathname.endsWith('.pdf')) {
      const newHeaders = new Headers(response.headers);
      
      // Point the PDF's canonical header to the HTML Archive Hub
      const canonicalUrl = 'https://regulatory-archive.kinslow.co/'; 
      newHeaders.set('Link', `<${canonicalUrl}>; rel="canonical"`);
      newHeaders.set('X-Robots-Tag', 'index, follow');

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders
      });
    }

    return response;
  }
}
