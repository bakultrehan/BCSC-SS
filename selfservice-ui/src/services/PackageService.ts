import axios from '@/lib/axios';
import { PackageModel } from '@/models/PackageModel';
import { PACKAGE_URL } from '@/config/api-endpoints';
export class PackageService {
  public static async getPackages() {
    return await axios.get(PACKAGE_URL + '/');
  }
}
