# PYXECM

A python library to interact with Opentext Extended ECM REST API.
The product API documentation is available on [OpenText Developer](https://developer.opentext.com/ce/products/extendedecm)
Detailed documentation of this package is available [here](https://opentext.github.io/pyxecm/).

# Quick start

Install pyxecm with the desired extras into your python environment, extra options are:

    - browserautomation
    - dataloader
    - sap

```bash
pip install pyxecm
```

## Start using the Customizer

Create an `.env` file as described here: [sample-environment-variables](customizerapisettings/#sample-environment-variables)

```bash
python -m pyxecm.customizer.api
```

??? example "Sample Output"
    ```console
    INFO:     Started server process [93861]
    INFO:     Waiting for application startup.
    31-Mar-2025 12:49:53 INFO [CustomizerAPI] [MainThread] Starting maintenance_page thread...
    31-Mar-2025 12:49:53 INFO [CustomizerAPI] [MainThread] Starting processing thread...
    31-Mar-2025 12:49:53 INFO [CustomizerAPI.payload_list] [customization_run_api] Starting 'Scheduler' thread for payload list processing...
    INFO:     Application startup complete.
    31-Mar-2025 12:49:53 INFO [CustomizerAPI.payload_list] [customization_run_api] Waiting for thread -> 'Scheduler' to complete...
    INFO:     Started server process [93861]
    INFO:     Waiting for application startup.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:5555 (Press CTRL+C to quit)
    ```

Access the Customizer API at [http://localhost:8000/api](http://localhost:8000/api)


## Start using the package libraries
```python
from pyxecm import OTCS

otcs_object = OTCS(
    protocol="https",
    hostname="otcs.domain.tld",
    port="443",
    public_url="otcs.domain.tld",
    username="admin",
    password="********",
    base_path="/cs/llisapi.dll",
)

otcs_object.authenticate()

nodes = otcs_object.get_subnodes(2000)

for node in nodes["results"]:
    print(node["data"]["properties"]["id"], node["data"]["properties"]["name"])
```
??? example "Sample Output"
    ```console
    13050 Administration
    13064 Case Management
    18565 Contract Management
    18599 Customer Support
    18536 Engineering & Construction
    13107 Enterprise Asset Management
    18632 Human Resources
    6554 Inbox Folders
    ```

# Disclaimer

!!! quote ""
    Copyright © 2025 Open Text Corporation, All Rights Reserved.
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
