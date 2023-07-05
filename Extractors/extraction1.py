import re
import whois
import tldextract
import time
from urllib.parse import urlparse, parse_qs
import requests
import ipwhois
import socket

class ExtractFeatures:
    def parse_url(self, url):
        """
        Parses the given URL and extracts various components.

        This method takes in URL input and parses it.
        It extracts the domain, directories, files and parameters (if applicable) of the URL.
        It also counts the number of top-level domains in the URL.

        Args:
            url (str): The URL to be parsed.

        Returns:
            tuple: A tuple containing the extracted components of the URL.
                - domain (str): The domain name of the URL.
                - directories (str): The directories in the URL's path.
                - file (str): The file name in the URL's path.
                - parameters (dict): A dictionary of query parameters.
                - num_tlds (int): The number of top-level domains in the URL.
        """
        # Parse the URL into its components
        if '//' not in url:
            url = '//' + url

        parsed_url = urlparse(url)

        # Extract the domain name
        domain = parsed_url.netloc

        # Extract the path and split it into directories and file name
        path = parsed_url.path
        directories, file = path.rsplit('/', 1) if '/' in path else (path, "")

        # Extract the query parameters
        parameters = parse_qs(parsed_url.query)

        tld_info = tldextract.extract(url)
        tld = tld_info.suffix

        # Count the number of top-level domains
        num_tlds = tld.count('.') + 1

        return domain, directories, file, parameters, num_tlds

    def get_domain_info(self, domain):
        """
        Retrieves information about a domain.

        This method takes in the domain of a URL as input, and fetches its information.
        It calculates the time elapsed since its creation and time remaining for its expiration.

        Args:
            domain (str): The domain to retrieve information for.

        Returns:
            tuple: A tuple containing the creation and expiration time of the domain in seconds.
                - creation_time_seconds (float): Time elapsed since domain creation in seconds.
                - expiration_time_seconds (float):  Time remaining for domain expiration in seconds.
        """
        try:
            # Get the domain information using python-whois
            domain_info = whois.whois(domain)

            # Extract the creation and expiration time
            creation_time = domain_info.creation_date
            expiration_time = domain_info.expiration_date

            # Convert the time to seconds
            if creation_time and expiration_time:
                creation_time_seconds = time.mktime(creation_time.timetuple())
                expiration_time_seconds = time.mktime(expiration_time.timetuple())
            else:
                raise ValueError
        except:
            creation_time_seconds = -1
            expiration_time_seconds = -1

        return creation_time_seconds, expiration_time_seconds
    
    def get_redirects(self, url):
        """
        Retrieves the number of redirects for a given URL.

        This method takes in a URL as input and assesses the number of times it redirects traffic.

        Args:
            url (str): The URL to retrieve redirects for.

        Returns:
            int: The number of redirects encountered.

        Note:
            The maximum number of redirects is limited to 20 to prevent infinite loops.
        """
        max_redirects = 20

        # Initialize the redirect count
        redirect_count = 0

        # Follow
