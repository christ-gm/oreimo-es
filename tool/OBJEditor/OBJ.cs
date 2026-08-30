using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace OBJEditor;

public class Obj(byte[] script, byte version) {
    byte Version = version;
    const byte vOREIMO = 1;

    private const short Dialogue = 0x64;
    private const short Dialogue2 = 0x68;

    private const short Choice = 0x69;
    private const short Choice2 = 0x67;

    private const short Question = 0x0323;

    private const short Chapter = 0x2BC;

    // Offset of the referenced block number inside the block types that hold one:
    // a jump (0x2BE) and an O.R.E. decision (0x515).
    private const int JumpTargetOffset = 0x06;
    private const int OreChoiceTargetOffset = 0x0E;

    public string[] Import() {
        List<string> strings = [];
        int blockCount = script.GetInt32(0x00);
        int blockLen = script.GetInt32(0x04);
//         Console.WriteLine($"Import: blockCount={blockCount}, blockLen={blockLen}");

        for (int i = blockLen, x = 0; x < blockCount; x++, i += blockLen) {
            blockLen = script.GetInt32(i);
            int index = i + 6;
            int entries;
            switch (script.GetInt16(i + 4)) {
                case Dialogue2:
                case Dialogue:
                    int textOffset = Version == vOREIMO ? 11 : 10;
                    strings.Add(script.GetString(i + textOffset));
                    break;

                case Choice:
                    entries = script.GetInt32(index);
                    for (int y = 0; y < entries; y++) {
                        index += 0x8;
                        strings.Add(script.GetString(index));
                        index += script.GetInt32(index) * 2 + 4;
                    }

                    break;

                case Choice2:
                    entries = script.GetInt32(index);
                    index += 0x8;

                    for (int y = 0; y < entries; y++) {
                        strings.Add(script.GetString(index));
                        index += script.GetInt32(index) * 2 + 4;

                        if (script.GetInt32(index) == 0x00) {
                            index += 8;
                        } else {
                            System.Diagnostics.Debug.Assert(script.GetInt32(index) == 0x01);

                            index += 4;
                            index += script.GetInt32(index) * 2 + 4;
                            index += 4;
                        }
                    }

                    break;

                case Question:
                    index += 4;
                    entries = script.GetInt32(index);
                    index += 4;

                    strings.Add(script.GetString(index));
                    index += 0x4 + script.GetInt32(index) * 2;

                    for (int y = 0; y < entries; y++) {
                        strings.Add(script.GetString(index));
                        index += 0x4 + script.GetInt32(index) * 2 + 0x24;
                    }

                    break;
                case Chapter:
                    strings.Add(script.GetString(index));
                    break;
            }
        }

        return strings.ToArray();
    }

    public byte[] Export(string[] strings) {
        int blockCount = script.GetInt32(0x00);
        int blockLen = script.GetInt32(0x04);
        List<List<int>> jumpUpdates = [];

        MemoryStream output = new();
        script.CopyTo(output, 0, blockLen);

        for (int i = blockLen, x = 0, id = 0; x < blockCount; x++, i += blockLen) {
            blockLen = script.GetInt32(i);
            MemoryStream newBlock;
            int index = i;
            int count;

            switch (script.GetInt16(i + 4)) {
                case Dialogue2:
                case Dialogue:
                    newBlock = new MemoryStream();
                    int textOffset = Version == vOREIMO ? 0x7 : 0x6;
                    script.CopyTo(newBlock, i + 4, textOffset);

                    string phrase = strings[id++];
                    string? secondPhrase = null;
                    if (phrase.Contains("[DEL]")) {
                        List<int> jumpInfo = [x, -1];
                        jumpUpdates.Add(jumpInfo);
                        x--;
                        blockCount--;
                        break;
                    }

                    if (phrase.Contains("[") && phrase.Contains("]")) {
                        secondPhrase = Regex.Match(phrase, @"\[(.*?)\]").Groups[1].Value;
                        phrase = phrase.Replace("[" + secondPhrase + "]", "");

                        if (phrase.Contains("（") && phrase.Contains("）"))
                            secondPhrase = "（" + secondPhrase + "）";
                        if (phrase.EndsWith("」"))
                            secondPhrase = phrase.Substring(0, phrase.IndexOf("「") + 1) + secondPhrase + "」";
                    }

                    phrase.WriteTo(newBlock);

                    WriteBlock(newBlock, output);
                    if (secondPhrase != null) {
                        newBlock = new MemoryStream();
                        script.CopyTo(newBlock, i + 4, Version == vOREIMO ? 0x3 : 0x2);
                        newBlock.Write([0xFF, 0xFF, 0xFF, 0xFF], 0, 4);

                        secondPhrase.WriteTo(newBlock);
                        WriteBlock(newBlock, output);

                        List<int> jumpInfo = [x, 1];
                        jumpUpdates.Add(jumpInfo);
                        x++;
                        blockCount++;
                    }

                    break;

                case Choice:
                    newBlock = new MemoryStream();
                    count = script.GetInt32(index + 0x6);
                    script.CopyTo(newBlock, index + 4, 0x2);
                    index += 0x06;

                    for (int y = 0; y < count; y++) {
                        script.CopyTo(newBlock, index, 0x8);
                        LimitString(strings[id++]).WriteTo(newBlock);

                        index += 0x8;
                        index += script.GetInt32(index) * 2 + 4;
                    }

                    WriteBlock(newBlock, output);
                    break;
                case Choice2:
                    newBlock = new MemoryStream();
                    index += 4;

                    count = script.GetInt32(index + 0x2);

                    script.CopyTo(newBlock, index, 0xA);
                    index += 0xA;


                    for (int y = 0; y < count; y++) {
                        LimitString(strings[id++]).WriteTo(newBlock);
                        index += script.GetInt32(index) * 2 + 4;


                        script.CopyTo(newBlock, index, 0x4);
                        index += 4;

                        if (script.GetInt32(index - 4) == 0x00) {
                            script.CopyTo(newBlock, index, 0x4);
                            index += 4;
                        } else {
                            int labelLen = script.GetInt32(index) * 2 + 4;
                            script.CopyTo(newBlock, index, labelLen);
                            index += labelLen;

                            script.CopyTo(newBlock, index, 0x4);
                            index += 4;
                        }
                    }

                    WriteBlock(newBlock, output);
                    break;

                case Question:
                    newBlock = new MemoryStream();

                    count = script.GetInt32(index + 0xA);
                    script.CopyTo(newBlock, index + 4, 0xA);
                    index += 0xE;

                    index += script.GetInt32(index) * 2 + 4;
                    LimitString(strings[id++]).WriteTo(newBlock);

                    for (int y = 0; y < count; y++) {
                        index += script.GetInt32(index) * 2 + 4;

                        LimitString(strings[id++]).WriteTo(newBlock);


                        script.CopyTo(newBlock, index, 0x24);
                        index += 0x24;
                    }

                    WriteBlock(newBlock, output);
                    break;

                case Chapter:
                    newBlock = new MemoryStream();
                    script.CopyTo(newBlock, index + 4, 0x2);

                    index += 0x6;
                    index += script.GetInt32(index) * 2 + 4;

                    strings[id++].WriteTo(newBlock);
                    script.CopyTo(newBlock, index, 0x6);

                    WriteBlock(newBlock, output);
                    break;

                default:
                    script.CopyTo(output, i, blockLen);
                    break;
            }
        }

        byte[] blockCountBytes = BitConverter.GetBytes(blockCount);
        output.Position = 0;
        output.Write(blockCountBytes, 0, blockCountBytes.Length);

        for (int i = 0; i < jumpUpdates.Count; i++)
            UpdateJumps(output, jumpUpdates[i][0], jumpUpdates[i][1]);

        return output.ToArray();
    }

    private void UpdateJumps(MemoryStream stream, int minBlock, int change) {
        stream.Seek(0, SeekOrigin.Begin);
        for (int i = 0; i < stream.Length; i += 16) {
            byte[] line = new byte[20];
            stream.Seek(i, SeekOrigin.Begin);
            int read = stream.Read(line, 0, 20);
            if (read < 16) break;

            // jump is 10 00 00 00 BE 02 xx xx xx xx 00 00 00 00 00 00, where "xx xx xx xx" is block number
            if (line[0] == 0x10 && line[1] == 0x00 && line[2] == 0x00 && line[3] == 0x00 && line[4] == 0xBE &&
                line[5] == 0x02) {
                UpdateBlockReference(stream, i + JumpTargetOffset, minBlock, change);
                continue;
            }

            // O.R.E. decision is 20 00 00 00 15 05 ... with the block the "accept" branch
            // continues at stored at 0x0E. That is a block reference just like a jump, so it
            // has to move too when a [ ] page split inserts a block before it - otherwise
            // accepting falls through into the "decline" branch.
            if (read >= 20 && line[0] == 0x20 && line[1] == 0x00 && line[2] == 0x00 && line[3] == 0x00 &&
                line[4] == 0x15 && line[5] == 0x05) {
                UpdateBlockReference(stream, i + OreChoiceTargetOffset, minBlock, change);
            }
        }
    }

    private void UpdateBlockReference(MemoryStream stream, long position, int minBlock, int change) {
        byte[] reference = new byte[4];
        stream.Seek(position, SeekOrigin.Begin);
        stream.Read(reference, 0, 4);

        // minBlock is the block that was split (or deleted); it keeps its own number,
        // only what comes after it moves. Using "<" here would drag a reference that
        // points AT that dialogue onto the continuation half, skipping its first part.
        int blockNumber = reference.GetInt32(0x00);
        if (blockNumber <= minBlock) return;

        BitConverter.GetBytes(blockNumber + change).CopyTo(reference, 0);
        stream.Seek(position, SeekOrigin.Begin);
        stream.Write(reference, 0, 4);
    }

    private string LimitString(string input) {
        string result = input.Replace("＿", " ");
        return result;
    }

    public void WriteBlock(Stream content, Stream output) {
        int newLen = (int)content.Length + 4;
        int blank = 0;

        while ((newLen + blank) % 0x10 != 0x00)
            blank++;

        if (blank <= 0x8)
            blank += 0x10;

        newLen += blank;
        BitConverter.GetBytes(newLen).CopyTo(output, 0, 4);
        content.Seek(0, 0);
        content.CopyTo(output);
        new byte[blank].CopyTo(output, 0, blank);
    }
}