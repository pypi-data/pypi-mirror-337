# ddrescue-bad-files

Parses file system images and identifies corrupted files
via correlation with bad block information
from GNU ddrescue map files.

## Backends

This tool currently supports the following backends:

 - [`PyCdlib`][pycdlib]

## License

ddrescue-bad-files - identify file corruption via GNU ddrescue maps
Copyright © 2025 Matheus Afonso Martins Moreira <matheus@matheusmoreira.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

[pycdlib]: https://pypi.org/project/pycdlib/
