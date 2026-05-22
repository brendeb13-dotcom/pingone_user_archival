import * as XLSX from 'xlsx';

export class ExportService {
  async excel(data: any[], name: string) {
    const { saveAs } = await import('file-saver');
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Data');
    saveAs(
      new Blob([XLSX.write(wb, { type: 'array', bookType: 'xlsx' })]),
      `${name}.xlsx`
    );
  }
}