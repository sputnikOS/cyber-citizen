defmodule ShodanSearch do
  @moduledoc """
  A CLI tool to search Shodan using Elixir.
  """

  @api_url "https://api.shodan.io/shodan/host/search"

  def main(args) do
    options = parse_args(args)

    case options do
      {:ok, opts} -> search_shodan(opts)
      {:error, message} -> IO.puts(message)
    end
  end

  defp parse_args(args) do
    Optimus.parse!(
      name: "shodan_search",
      description: "Search Shodan from the command line",
      version: "0.1.0",
      author: "Your Name",
      about: "A simple Shodan search CLI tool",
      allow_unknown_args: false,
      parse_double_dash: true,
      args: [
        api_key: [value_name: "API_KEY", help: "Shodan API key", required: true],
        query: [value_name: "QUERY", help: "Search query", required: true]
      ],
      options: [
        facets: [
          short: "-f",
          long: "--facets",
          value_name: "FACETS",
          help: "Comma-separated list of facets to retrieve",
          default: ""
        ],
        limit: [
          short: "-l",
          long: "--limit",
          value_name: "LIMIT",
          help: "Limit the number of results",
          default: 10,
          parser: &parse_integer/1
        ]
      ]
    ).parse(args)
  end

  defp parse_integer(str) do
    case Integer.parse(str) do
      {int, ""} -> {:ok, int}
      _ -> {:error, "not an integer"}
    end
  end

  defp search_shodan(opts) do
    url = "#{@api_url}?key=#{opts.api_key}&query=#{opts.query}&facets=#{opts.facets}&limit=#{opts.limit}"

    case HTTPoison.get(url) do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} ->
        handle_response(body)

      {:ok, %HTTPoison.Response{status_code: status_code}} ->
        IO.puts("Failed to fetch data: HTTP #{status_code}")

      {:error, %HTTPoison.Error{reason: reason}} ->
        IO.puts("Request error: #{reason}")
    end
  end

  defp handle_response(body) do
    case Jason.decode(body) do
      {:ok, %{"total" => total, "matches" => matches, "facets" => facets}} ->
        IO.puts("Results found: #{total}")

        Enum.each(matches, fn match ->
          IO.puts("IP: #{match["ip_str"]}")
          IO.puts("Port: #{match["port"]}")
          IO.puts("Hostnames: #{Enum.join(match["hostnames"], ", ")}")
          IO.puts("Location: #{format_location(match["location"])}")
          IO.puts("Data: #{match["data"]}")
          IO.puts(String.duplicate("-", 60))
        end)

        if facets do
          IO.puts("Facets:")
          IO.puts(Jason.encode!(facets, pretty: true))
        end

      {:error, reason} ->
        IO.puts("Failed to parse response: #
